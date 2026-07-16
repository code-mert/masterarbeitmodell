"""
baselines.py

Eigenständiges Modul für Baseline-Vorhersagen (Random & Leave-One-Out Majority)
in der Wunde-Evaluationspipeline.

Re-verwendet die bestehende Metrik-Pipeline aus eval/metrics.py und eval/mapping.py.
"""

import os
import re
import random
import logging
from typing import Dict, Any, List, Set, Tuple, Optional
import numpy as np
import pandas as pd

from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids
from eval.mapping import align, filter_markers, unpack_value
from eval.normalize import to_set
from eval.metrics import set_f1, exact_match, best_path_f1, precision_recall

logger = logging.getLogger(__name__)

# Standard-Katalogdateien
DEFAULT_CATALOG_FILES = {
    "debridement": "lr0_produktkatalog.md",
    "primaerverband": "lr1_produktkatalog.md",
    "sekundaerverband": "lr2_produktkatalog.md",
    "kompression": "lr3_produktkatalog.md"
}

# Ordinales Mapping für Exsudatmenge
EXSUDAT_LEVELS = [
    ("sehr stark", 4),
    ("sehrmaessig", 3),
    ("stark", 3),
    ("mäßig", 2),
    ("maessig", 2),
    ("mittel", 2),
    ("leicht", 1),
    ("gering", 1),
    ("keine", 0),
]

EXSUDAT_OPTIONS = ["Keine", "Leicht", "Mäßig", "Stark", "Sehr stark"]


def resolve_path(rel_path: str) -> str:
    """
    Sucht robust nach dem übergebenen Pfad ausgehend vom aktuellen Arbeitsverzeichnis
    oder dem Projekt-Root.
    """
    if os.path.isabs(rel_path) and os.path.exists(rel_path):
        return rel_path
    if os.path.exists(rel_path):
        return os.path.abspath(rel_path)
        
    current = os.path.abspath(os.path.dirname(__file__))
    for _ in range(5):
        if os.path.exists(os.path.join(current, "data")):
            cleaned_rel = rel_path.replace("../", "")
            full = os.path.join(current, cleaned_rel)
            if os.path.exists(full):
                return full
        current = os.path.dirname(current)
        
    return os.path.abspath(rel_path)


def parse_markdown_h3_headers(file_path: str) -> List[str]:
    """Extrahiert alle H3-Überschriften (### Produktname) aus einer Markdown-Katalogdatei."""
    resolved = resolve_path(file_path)
    if not os.path.exists(resolved):
        logger.warning(f"Katalogdatei nicht gefunden: {resolved}")
        return []
    
    with open(resolved, "r", encoding="utf-8") as f:
        text = f.read()
        
    headers = re.findall(r"^###\s+(.*)", text, re.MULTILINE)
    return [h.strip() for h in headers if h.strip()]


def load_lr_catalog_pools(catalog_dir: str = "data/l&r_produktkatalog") -> Dict[str, List[str]]:
    """
    Lädt alle feldspezifischen Pools aus den L&R Markdown-Katalogdateien.
    
    Returns:
        Dict mit Listen der Produktnamen für 'debridement', 'primaerverband',
        'sekundaerverband' und 'kompression'.
    """
    pools = {}
    for field, filename in DEFAULT_CATALOG_FILES.items():
        full_path = os.path.join(catalog_dir, filename)
        pools[field] = parse_markdown_h3_headers(full_path)
    return pools


UNASSESSABLE_EXSUDAT_PHRASES = [
    "keine angabe",
    "keine einschätzung",
    "nicht beurteilbar",
    "nicht zu beschreiben",
    "nicht zu beurteilen"
]

def parse_exsudat_level(val: Any) -> Optional[int]:
    """Konvertiert eine Exsudatangabe in einen ordinalen Rang (0..4). Unbeurteilbare Angaben liefern None."""
    if val is None or pd.isna(val):
        return None
    val_str = str(val).strip().lower()
    if not val_str:
        return None
    
    # Prüfe zuerst auf unbeurteilbare Phrasen
    if any(phrase in val_str for phrase in UNASSESSABLE_EXSUDAT_PHRASES):
        return None
    
    for key, level in EXSUDAT_LEVELS:
        if key in val_str:
            return level
    return None


def calculate_qwk(y_true: List[Optional[int]], y_pred: List[Optional[int]], min_rating: int = 0, max_rating: int = 4) -> float:
    """
    Berechnet Quadratic Weighted Kappa (QWK) für zwei geordnete Sequenzen.
    Ignores Paare mit None-Werten.
    """
    valid_pairs = [(t, p) for t, p in zip(y_true, y_pred) if t is not None and p is not None]
    if not valid_pairs:
        return 0.0
    
    t_arr = np.array([pair[0] for pair in valid_pairs], dtype=int)
    p_arr = np.array([pair[1] for pair in valid_pairs], dtype=int)
    
    num_ratings = max_rating - min_rating + 1
    
    conf_mat = np.zeros((num_ratings, num_ratings), dtype=float)
    for t, p in zip(t_arr, p_arr):
        t_idx = int(np.clip(t - min_rating, 0, num_ratings - 1))
        p_idx = int(np.clip(p - min_rating, 0, num_ratings - 1))
        conf_mat[t_idx, p_idx] += 1.0
        
    w = np.zeros((num_ratings, num_ratings), dtype=float)
    for i in range(num_ratings):
        for j in range(num_ratings):
            w[i, j] = ((i - j) ** 2) / ((num_ratings - 1) ** 2)
            
    hist_true = np.bincount(np.clip(t_arr - min_rating, 0, num_ratings - 1), minlength=num_ratings)
    hist_pred = np.bincount(np.clip(p_arr - min_rating, 0, num_ratings - 1), minlength=num_ratings)
    
    expected = np.outer(hist_true, hist_pred) / float(len(t_arr))
    
    num = np.sum(w * conf_mat)
    den = np.sum(w * expected)
    if den == 0:
        return 1.0
    return float(1.0 - (num / den))


def _ensure_list(val: Any) -> List[str]:
    """Konvertiert Einzelwerte, Listen oder String-Darstellungen von Listen in Python-Listen."""
    if val is None:
        return []
    if isinstance(val, (list, tuple, set)):
        return [str(x).strip() for x in val if x is not None and not (isinstance(x, float) and np.isnan(x)) and str(x).strip()]
    if isinstance(val, (float, int)) and pd.isna(val):
        return []
    val_str = str(val).strip()
    if not val_str or val_str.lower() == "nan":
        return []
    if val_str.startswith("[") and val_str.endswith("]"):
        try:
            import ast
            parsed = ast.literal_eval(val_str)
            if isinstance(parsed, (list, tuple, set)):
                return [str(x).strip() for x in parsed if x is not None and str(x).strip()]
        except Exception:
            pass
    return [val_str]


def extract_gt_field_value(gt_rec: Dict[str, Any], field: str) -> Tuple[List[str], List[str]]:
    """
    Extrahiert für ein bestimmtes Evaluierungsfeld die GT-Set(s) / Werte aus einem GT-Record.
    
    Returns:
        (primary_list, secondary_list) -> für Pair-Felder (Wundauflage) primär & alt,
        für einfache Felder secondary_list = [].
    """
    if field == "primaerverband":
        p = filter_markers(_ensure_list(gt_rec.get("praeferenz_produkt")))
        a = filter_markers(_ensure_list(gt_rec.get("alternative_produkt")))
        return p, a
    elif field == "sekundaerverband":
        p = filter_markers(_ensure_list(gt_rec.get("ergaenzende_produkte_praeferenz")))
        a = filter_markers(_ensure_list(gt_rec.get("ergaenzende_produkte_alternativ")))
        return p, a
    elif field == "debridement":
        return filter_markers(_ensure_list(gt_rec.get("debridement"))), []
    elif field == "kompression":
        return filter_markers(_ensure_list(gt_rec.get("kompression_produkte"))), []
    elif field == "lokalisation":
        val = unpack_value(gt_rec.get("lokalisation"))
        return [val] if val else [], []
    elif field == "exsudatmenge":
        val = unpack_value(gt_rec.get("exsudat"))
        return ([val] if val and parse_exsudat_level(val) is not None else []), []
    else:
        return [], []



def generate_majority_predictions_loo(gt_records: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Generiert Leave-One-Out (LOO) Majority-Vorhersagen für alle Bilder in gt_records.
    Für jedes Bild i werden die am häufigsten vorkommenden GT-Werte aus allen Bildern j != i ermittelt.
    Für Set-Felder wird genau das Top-k Vorhersageset gewählt (Oracle-k, k = len(gt[i])).
    
    Returns:
        Dict[image_id, fake_llm_record]
    """
    image_ids = list(gt_records.keys())
    majority_preds = {}
    
    for target_id in image_ids:
        # 1. Training-Set ohne das Zielbild (Leave-One-Out)
        train_ids = [img_id for img_id in image_ids if img_id != target_id]
        
        # Häufigkeitszähler pro Feld
        counts = {
            "debridement": {},
            "praeferenz_wundauflage": {},
            "alternativ_wundauflage": {},
            "praeferenz_ergaenzung": {},
            "alternativ_ergaenzung": {},
            "kompression_produkt": {},
            "lokalisation": {},
            "exsudat_menge": {}
        }
        
        for train_id in train_ids:
            rec = gt_records[train_id]
            
            # Debridement
            for item in filter_markers(_ensure_list(rec.get("debridement"))):
                counts["debridement"][item] = counts["debridement"].get(item, 0) + 1
                
            # Wundauflagen
            for item in filter_markers(_ensure_list(rec.get("praeferenz_produkt"))):
                counts["praeferenz_wundauflage"][item] = counts["praeferenz_wundauflage"].get(item, 0) + 1
            for item in filter_markers(_ensure_list(rec.get("alternative_produkt"))):
                counts["alternativ_wundauflage"][item] = counts["alternativ_wundauflage"].get(item, 0) + 1
                
            # Sekundärverband
            for item in filter_markers(_ensure_list(rec.get("ergaenzende_produkte_praeferenz"))):
                counts["praeferenz_ergaenzung"][item] = counts["praeferenz_ergaenzung"].get(item, 0) + 1
            for item in filter_markers(_ensure_list(rec.get("ergaenzende_produkte_alternativ"))):
                counts["alternativ_ergaenzung"][item] = counts["alternativ_ergaenzung"].get(item, 0) + 1
                
            # Kompression
            for item in filter_markers(_ensure_list(rec.get("kompression_produkte"))):
                counts["kompression_produkt"][item] = counts["kompression_produkt"].get(item, 0) + 1
                
            # Kategorial
            lok = unpack_value(rec.get("lokalisation"))
            if lok:
                counts["lokalisation"][lok] = counts["lokalisation"].get(lok, 0) + 1
                
            exs = unpack_value(rec.get("exsudat"))
            if exs:
                counts["exsudat_menge"][exs] = counts["exsudat_menge"].get(exs, 0) + 1

        # Hilfsfunktion zur Auswahl der Top-k häufigsten Elemente
        def get_top_k(count_dict: Dict[str, int], k: int) -> List[str]:
            if k <= 0:
                return []
            sorted_items = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
            return [item for item, _ in sorted_items[:k]]

        # Hilfsfunktion zur Auswahl der Top-1 Kategorie
        def get_top_1(count_dict: Dict[str, int]) -> str:
            if not count_dict:
                return ""
            return sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))[0][0]

        # 2. Oracle-k Setgrößen für das Zielbild ermitteln
        target_rec = gt_records[target_id]
        
        gt_deb, _ = extract_gt_field_value(target_rec, "debridement")
        gt_prim_p, gt_prim_a = extract_gt_field_value(target_rec, "primaerverband")
        gt_sek_p, gt_sek_a = extract_gt_field_value(target_rec, "sekundaerverband")
        gt_komp, _ = extract_gt_field_value(target_rec, "kompression")
        
        # Fake LLM-Record strukturieren
        fake_rec = {
            "image_id": target_id,
            "debridement_methode": get_top_k(counts["debridement"], len(gt_deb)),
            "praeferenz_wundauflage": get_top_k(counts["praeferenz_wundauflage"], len(gt_prim_p)),
            "alternativ_wundauflage": get_top_k(counts["alternativ_wundauflage"], len(gt_prim_a)),
            "praeferenz_ergaenzung": get_top_k(counts["praeferenz_ergaenzung"], len(gt_sek_p)),
            "alternativ_ergaenzung": get_top_k(counts["alternativ_ergaenzung"], len(gt_sek_a)),
            "kompression_produkt": get_top_k(counts["kompression_produkt"], len(gt_komp)),
            "lokalisation": get_top_1(counts["lokalisation"]),
            "exsudat_menge": get_top_1(counts["exsudat_menge"])
        }
        majority_preds[target_id] = fake_rec
        
    return majority_preds


def generate_random_prediction_single_run(
    gt_records: Dict[str, Dict[str, Any]],
    pools: Dict[str, List[str]],
    lokalisation_pool: List[str],
    exsudat_pool: List[str],
    rng: random.Random
) -> Dict[str, Dict[str, Any]]:
    """
    Generiert einen einzelnen Random-Baseline-Durchlauf für alle Bilder unter Nutzung von Oracle-k.
    Zieht gleichverteilt ohne Zurücklegen aus den feldspezifischen Katalog- / Kategoriensets.
    """
    random_preds = {}
    
    for img_id, rec in gt_records.items():
        gt_deb, _ = extract_gt_field_value(rec, "debridement")
        gt_prim_p, gt_prim_a = extract_gt_field_value(rec, "primaerverband")
        gt_sek_p, gt_sek_a = extract_gt_field_value(rec, "sekundaerverband")
        gt_komp, _ = extract_gt_field_value(rec, "kompression")
        
        def sample_from_pool(pool: List[str], k: int) -> List[str]:
            if k <= 0 or not pool:
                return []
            k_sample = min(k, len(pool))
            return rng.sample(pool, k_sample)
            
        fake_rec = {
            "image_id": img_id,
            "debridement_methode": sample_from_pool(pools.get("debridement", []), len(gt_deb)),
            "praeferenz_wundauflage": sample_from_pool(pools.get("primaerverband", []), len(gt_prim_p)),
            "alternativ_wundauflage": sample_from_pool(pools.get("primaerverband", []), len(gt_prim_a)),
            "praeferenz_ergaenzung": sample_from_pool(pools.get("sekundaerverband", []), len(gt_sek_p)),
            "alternativ_ergaenzung": sample_from_pool(pools.get("sekundaerverband", []), len(gt_sek_a)),
            "kompression_produkt": sample_from_pool(pools.get("kompression", []), len(gt_komp)),
            "lokalisation": rng.choice(lokalisation_pool) if lokalisation_pool else "",
            "exsudat_menge": rng.choice(exsudat_pool) if exsudat_pool else ""
        }
        random_preds[img_id] = fake_rec
        
    return random_preds


def evaluate_single_dataset_pair(
    gt_data: Dict[str, Dict[str, Any]],
    pred_data: Dict[str, Dict[str, Any]],
    matched_ids: List[str]
) -> Tuple[Dict[str, float], Dict[str, Dict[str, float]]]:
    """
    Wertet ein Vorhersageset (LLM, Majority oder Random-Run) gegen ein Ground Truth Set aus.
    Benutzt exakt align(), best_path_f1(), set_f1(), exact_match() und calculate_qwk().
    
    Returns:
        (macro_scores, per_image_scores)
    """
    fields = ["lokalisation", "exsudatmenge", "debridement", "primaerverband", "sekundaerverband", "kompression"]
    
    per_image_scores = {field: {} for field in fields}
    
    exs_gt_levels = []
    exs_pred_levels = []
    
    for img_id in matched_ids:
        gt_rec = gt_data[img_id]
        pred_rec = pred_data.get(img_id, {})
        
        aligned = align(gt_rec, pred_rec)
        
        # 1. Lokalisation (Accuracy / Exact Match)
        gt_lok = unpack_value(gt_rec.get("lokalisation"))
        pred_lok = unpack_value(pred_rec.get("lokalisation"))
        lok_acc = 1.0 if (gt_lok and pred_lok and gt_lok.strip().lower() == pred_lok.strip().lower()) or (not gt_lok and not pred_lok) else 0.0
        per_image_scores["lokalisation"][img_id] = lok_acc
        
        # 2. Exsudatmenge (Ordinale Ränge sammeln für QWK)
        gt_exs = unpack_value(gt_rec.get("exsudat"))
        pred_exs = unpack_value(pred_rec.get("exsudat_menge") or pred_rec.get("exsudat"))
        exs_gt_levels.append(parse_exsudat_level(gt_exs))
        exs_pred_levels.append(parse_exsudat_level(pred_exs))
        
        gt_l = parse_exsudat_level(gt_exs)
        pr_l = parse_exsudat_level(pred_exs)
        if gt_l is not None and pr_l is not None:
            per_image_scores["exsudatmenge"][img_id] = 1.0 - (abs(gt_l - pr_l) / 4.0)
        else:
            per_image_scores["exsudatmenge"][img_id] = 1.0 if gt_exs == pred_exs else 0.0
            
        # 3. Primärverband (best_path_f1)
        llm_p = to_set(aligned["primaerverband"]["llm_praef"])
        llm_a = to_set(aligned["primaerverband"]["llm_alt"])
        gt_p = to_set(aligned["primaerverband"]["gt_praef"])
        gt_a = to_set(aligned["primaerverband"]["gt_alt"])
        f1_prim, _, _, _ = best_path_f1(llm_p, llm_a, gt_p, gt_a)
        per_image_scores["primaerverband"][img_id] = f1_prim
        
        # 4. Débridement (set_f1)
        llm_deb = to_set(aligned["debridement"]["llm"])
        gt_deb = to_set(aligned["debridement"]["gt"])
        per_image_scores["debridement"][img_id] = set_f1(llm_deb, gt_deb)
        
        # 5. Sekundärverband (best_path_f1 / set_f1)
        if "llm_praef" in aligned["sekundaerverband"]:
            llm_p_s = to_set(aligned["sekundaerverband"]["llm_praef"])
            llm_a_s = to_set(aligned["sekundaerverband"]["llm_alt"])
            gt_p_s = to_set(aligned["sekundaerverband"]["gt_praef"])
            gt_a_s = to_set(aligned["sekundaerverband"]["gt_alt"])
            f1_sek, _, _, _ = best_path_f1(llm_p_s, llm_a_s, gt_p_s, gt_a_s)
            per_image_scores["sekundaerverband"][img_id] = f1_sek
        else:
            llm_sek = to_set(aligned["sekundaerverband"]["llm"])
            gt_sek = to_set(aligned["sekundaerverband"]["gt"])
            per_image_scores["sekundaerverband"][img_id] = set_f1(llm_sek, gt_sek)
            
        # 6. Kompression (set_f1)
        llm_komp = to_set(aligned["kompression"]["llm"])
        gt_komp = to_set(aligned["kompression"]["gt"])
        per_image_scores["kompression"][img_id] = set_f1(llm_komp, gt_komp)
        
    # Makro-Scores aggragieren
    macro_scores = {}
    for f in ["lokalisation", "debridement", "primaerverband", "sekundaerverband", "kompression"]:
        vals = list(per_image_scores[f].values())
        macro_scores[f] = float(np.mean(vals)) if vals else 0.0
        
    # QWK und Distance Score für Exsudatmenge über die gesamte Stichprobe
    macro_scores["exsudatmenge"] = calculate_qwk(exs_gt_levels, exs_pred_levels)
    exs_dist_vals = list(per_image_scores["exsudatmenge"].values())
    macro_scores["exsudatmenge_dist"] = float(np.mean(exs_dist_vals)) if exs_dist_vals else 0.0
    
    return macro_scores, per_image_scores


class BaselineEvaluator:
    """
    Hauptklasse zur Durchführung der dualen Baseline-Evaluation gegen Experte 1 & Experte 2.
    """
    
    def __init__(
        self,
        gt1_path: str = "data/ground_truth/lohmann_rauscher/Experte1_LR_GroundTruth_normalised.csv",
        gt2_path: Optional[str] = "data/ground_truth/lohmann_rauscher/Experte2_LR_GroundTruth_normalised.csv",
        catalog_dir: str = "data/l&r_produktkatalog"
    ):
        res_gt1 = resolve_path(gt1_path)
        res_gt2 = resolve_path(gt2_path) if gt2_path else None
        res_cat = resolve_path(catalog_dir)
        
        self.gt1 = load_ground_truth(res_gt1)
        self.gt2 = load_ground_truth(res_gt2) if res_gt2 and os.path.exists(res_gt2) else None
        self.catalog_dir = res_cat
        self.pools = load_lr_catalog_pools(res_cat)
        
        # Pools für Kategorialfelder ermitteln
        self.lokalisation_pool = self._extract_lokalisation_pool()
        self.exsudat_pool = EXSUDAT_OPTIONS.copy()
        
    def _extract_lokalisation_pool(self) -> List[str]:
        lok_set = set()
        for gt in [self.gt1, self.gt2]:
            if not gt:
                continue
            for rec in gt.values():
                val = unpack_value(rec.get("lokalisation"))
                if val and val != "?" and "keine" not in val.lower() and "nicht" not in val.lower():
                    lok_set.add(val)
        return sorted(list(lok_set)) if lok_set else ["Abdomen", "Arm", "Bein", "Fuß", "Gesäß", "Hand"]

    def audit_gt_catalog_coverage(self, gt_data: Dict[str, Dict[str, Any]], expert_name: str = "Experte 1") -> Dict[str, Any]:
        """
        Analysiert GT-Einträge auf Abdeckung durch den Teilkatalog und gibt Warnungen aus.
        Ermittelt non_catalog_rate und n_empty pro Feld.
        """
        stats = {}
        fields = ["lokalisation", "exsudatmenge", "debridement", "primaerverband", "sekundaerverband", "kompression"]
        
        for f in fields:
            pool = set(self.pools.get(f, []))
            total_items = 0
            non_cat_items = 0
            empty_count = 0
            
            for img_id, rec in gt_data.items():
                p_items, a_items = extract_gt_field_value(rec, f)
                all_items = p_items + a_items
                
                if not all_items:
                    empty_count += 1
                else:
                    if f in self.pools:
                        for it in all_items:
                            total_items += 1
                            if it not in pool:
                                non_cat_items += 1
                                logger.warning(f"[{expert_name}] GT-Produkt '{it}' in Bild {img_id} (Feld '{f}') IST NICHT IM TEILKATALOG.")
                                
            rate = (non_cat_items / total_items) if total_items > 0 else 0.0
            stats[f] = {
                "n_empty": empty_count,
                "total_items": total_items,
                "non_catalog_items": non_cat_items,
                "non_catalog_rate": rate
            }
            
        return stats

    def run_evaluation(
        self,
        llm_path_or_dict: Any,
        n_runs: int = 1000,
        seed: int = 42,
        filter_non_catalog: bool = False
    ) -> Dict[str, Any]:
        """
        Führt die vollständige duale Evaluierung durch.
        """
        # LLM-Outputs laden
        if isinstance(llm_path_or_dict, str):
            res_llm = resolve_path(llm_path_or_dict)
            llm_data = load_llm_outputs(res_llm)
        else:
            llm_data = llm_path_or_dict

        matched_ids1 = matched_image_ids(self.gt1, llm_data) if llm_data else sorted(list(self.gt1.keys()))
        matched_ids2 = matched_image_ids(self.gt2, llm_data) if (self.gt2 and llm_data) else (sorted(list(self.gt2.keys())) if self.gt2 else [])

        audit1 = self.audit_gt_catalog_coverage(self.gt1, "Experte 1")
        audit2 = self.audit_gt_catalog_coverage(self.gt2, "Experte 2") if self.gt2 else None

        eval_gt1 = self._apply_catalog_filter(self.gt1) if filter_non_catalog else self.gt1
        eval_gt2 = (self._apply_catalog_filter(self.gt2) if filter_non_catalog else self.gt2) if self.gt2 else None

        # 1. Majority-Baseline (LOO)
        maj_pred1 = generate_majority_predictions_loo(eval_gt1)
        maj_scores1, maj_per_img1 = evaluate_single_dataset_pair(eval_gt1, maj_pred1, matched_ids1)

        maj_scores2, maj_per_img2 = None, None
        if eval_gt2:
            maj_pred2 = generate_majority_predictions_loo(eval_gt2)
            maj_scores2, maj_per_img2 = evaluate_single_dataset_pair(eval_gt2, maj_pred2, matched_ids2)

        # 2. Random-Baseline (1000 Runs)
        rng = random.Random(seed)
        all_fields = ["lokalisation", "exsudatmenge", "exsudatmenge_dist", "debridement", "primaerverband", "sekundaerverband", "kompression"]
        rand_runs_scores1 = {f: [] for f in all_fields}
        rand_runs_scores2 = {f: [] for f in all_fields} if eval_gt2 else None

        for r in range(n_runs):
            rand_pred1 = generate_random_prediction_single_run(eval_gt1, self.pools, self.lokalisation_pool, self.exsudat_pool, rng)
            scores1, _ = evaluate_single_dataset_pair(eval_gt1, rand_pred1, matched_ids1)
            for f, sc in scores1.items():
                rand_runs_scores1[f].append(sc)

            if eval_gt2:
                rand_pred2 = generate_random_prediction_single_run(eval_gt2, self.pools, self.lokalisation_pool, self.exsudat_pool, rng)
                scores2, _ = evaluate_single_dataset_pair(eval_gt2, rand_pred2, matched_ids2)
                for f, sc in scores2.items():
                    rand_runs_scores2[f].append(sc)

        rand_summary1 = {}
        for f, arr in rand_runs_scores1.items():
            mean_v = float(np.mean(arr))
            p2_5 = float(np.percentile(arr, 2.5))
            p97_5 = float(np.percentile(arr, 97.5))
            rand_summary1[f] = {
                "mean": mean_v,
                "ci_low": p2_5,
                "ci_high": p97_5,
                "str": f"{mean_v:.3f} [{p2_5:.3f}, {p97_5:.3f}]"
            }

        rand_summary2 = {}
        if rand_runs_scores2:
            for f, arr in rand_runs_scores2.items():
                mean_v = float(np.mean(arr))
                p2_5 = float(np.percentile(arr, 2.5))
                p97_5 = float(np.percentile(arr, 97.5))
                rand_summary2[f] = {
                    "mean": mean_v,
                    "ci_low": p2_5,
                    "ci_high": p97_5,
                    "str": f"{mean_v:.3f} [{p2_5:.3f}, {p97_5:.3f}]"
                }

        # 3. LLM-Evaluierung
        llm_scores1, llm_per_img1 = evaluate_single_dataset_pair(eval_gt1, llm_data, matched_ids1) if llm_data else ({}, {})
        llm_scores2, llm_per_img2 = (evaluate_single_dataset_pair(eval_gt2, llm_data, matched_ids2) if (eval_gt2 and llm_data) else ({}, {}))

        # 4. Inter-Rater (Experte 1 vs Experte 2)
        inter_rater_scores, inter_per_img = ({}, {})
        if eval_gt2:
            common_ids = sorted(list(set(eval_gt1.keys()).intersection(set(eval_gt2.keys()))))
            inter_rater_scores, inter_per_img = evaluate_single_dataset_pair(eval_gt1, eval_gt2, common_ids)

        fields_config = [
            ("lokalisation", "Accuracy"),
            ("exsudatmenge", "QWK"),
            ("exsudatmenge_dist", "Distance Score"),
            ("debridement", "Macro-F1"),
            ("primaerverband", "Macro-F1"),
            ("sekundaerverband", "Macro-F1"),
            ("kompression", "Macro-F1")
        ]

        summary_rows = []
        for f, metric_name in fields_config:
            audit_key = "exsudatmenge" if f.startswith("exsudatmenge") else f
            row = {
                "Feld": f,
                "Metrik": metric_name,
                "GT1 Random (Mean [95% CI])": rand_summary1[f]["str"],
                "GT1 Majority": maj_scores1.get(f, np.nan),
                "GT1 LLM": llm_scores1.get(f, np.nan),
            }
            
            if eval_gt2:
                row["GT2 Random (Mean [95% CI])"] = rand_summary2[f]["str"]
                row["GT2 Majority"] = maj_scores2.get(f, np.nan)
                row["GT2 LLM"] = llm_scores2.get(f, np.nan)
                row["Experte 1 vs Experte 2 (Inter-Rater)"] = inter_rater_scores.get(f, np.nan)
            
            row["GT1 n_empty"] = audit1[audit_key]["n_empty"]
            row["GT1 non_catalog_rate"] = f"{audit1[audit_key]['non_catalog_rate']:.1%}"
            
            if audit2:
                row["GT2 n_empty"] = audit2[audit_key]["n_empty"]
                row["GT2 non_catalog_rate"] = f"{audit2[audit_key]['non_catalog_rate']:.1%}"
                
            summary_rows.append(row)

        df_summary = pd.DataFrame(summary_rows)

        all_ids = matched_ids1
        per_img_rows = []
        for img_id in all_ids:
            row = {"image_id": img_id}
            for f, _ in fields_config:
                row[f"{f}_llm_vs_gt1"] = llm_per_img1.get(f, {}).get(img_id, np.nan)
                row[f"{f}_maj_vs_gt1"] = maj_per_img1.get(f, {}).get(img_id, np.nan)
                if eval_gt2:
                    row[f"{f}_llm_vs_gt2"] = llm_per_img2.get(f, {}).get(img_id, np.nan)
                    row[f"{f}_maj_vs_gt2"] = maj_per_img2.get(f, {}).get(img_id, np.nan)
                    row[f"{f}_gt1_vs_gt2"] = inter_per_img.get(f, {}).get(img_id, np.nan)
            per_img_rows.append(row)

        df_per_image = pd.DataFrame(per_img_rows)

        return {
            "summary_table": df_summary,
            "per_image_table": df_per_image,
            "gt1_audit": audit1,
            "gt2_audit": audit2,
            "rand_summary1": rand_summary1,
            "rand_summary2": rand_summary2,
            "maj_scores1": maj_scores1,
            "maj_scores2": maj_scores2,
            "llm_scores1": llm_scores1,
            "llm_scores2": llm_scores2,
            "inter_rater_scores": inter_rater_scores
        }

    def _apply_catalog_filter(self, gt_data: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Filtert GT-Einträge heraus, die nicht im zugehörigen Katalog enthalten sind (für Sensitivitätsanalyse)."""
        filtered_gt = {}
        for img_id, rec in gt_data.items():
            new_rec = rec.copy()
            for f, col_names in [
                ("debridement", ["debridement"]),
                ("primaerverband", ["praeferenz_produkt", "alternative_produkt"]),
                ("sekundaerverband", ["ergaenzende_produkte_praeferenz", "ergaenzende_produkte_alternativ"]),
                ("kompression", ["kompression_produkte"])
            ]:
                pool = set(self.pools.get(f, []))
                for col in col_names:
                    if col in new_rec and new_rec[col]:
                        lst = filter_markers(new_rec[col] if isinstance(new_rec[col], list) else [new_rec[col]])
                        valid = [item for item in lst if item in pool]
                        new_rec[col] = valid
            filtered_gt[img_id] = new_rec
        return filtered_gt


def evaluate_baselines_dual(
    gt1_path_or_dict: Any,
    gt2_path_or_dict: Any,
    llm_path_or_dict: Any,
    catalog_dir: str = "data/l&r_produktkatalog",
    n_runs: int = 1000,
    seed: int = 42,
    filter_non_catalog: bool = False
) -> Dict[str, Any]:
    """
    Bequeme Top-Level-Funktion zur Ausführung der dualen Baseline-Evaluierung aus dem Notebook.
    """
    if isinstance(gt1_path_or_dict, str):
        evaluator = BaselineEvaluator(gt1_path=gt1_path_or_dict, gt2_path=gt2_path_or_dict, catalog_dir=catalog_dir)
    else:
        evaluator = BaselineEvaluator(catalog_dir=catalog_dir)
        evaluator.gt1 = gt1_path_or_dict
        evaluator.gt2 = gt2_path_or_dict if isinstance(gt2_path_or_dict, dict) else None
        
    return evaluator.run_evaluation(llm_path_or_dict, n_runs=n_runs, seed=seed, filter_non_catalog=filter_non_catalog)
