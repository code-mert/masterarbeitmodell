"""
primaerverband_baselines.py

Random- und Majority-Baseline für die Primärverband-Empfehlung (L&R-Katalog),
getrennt pro Experte und pro Level.

Die Baselines verwenden exakt dieselbe Bewertung wie die KI-Scores in primaerverband_calc.py
(Best-Path-F1, map_level_2 / map_level_3, gleiche Ausschlussregeln), damit die Werte direkt
mit calculate_primaerverband_lr_expert_scores() vergleichbar sind.

Random-Baseline
    Für jede Wunde wird ein zufälliges Präferenz-Set und ein zufälliges Alternativ-Set aus den
    32 Primärverbänden des Katalogs (lr1_produktkatalog.md) gezogen – ohne Zurücklegen innerhalb
    eines Sets, beide Sets unabhängig voneinander. Die Set-Größen entsprechen denen der KI
    (Two-Stage) an derselben Wunde, damit der Zufall dieselbe Anzahl an „Versuchen“ hat wie die KI.
    Statt zu simulieren wird der exakte Erwartungswert berechnet: Alle möglichen Sets werden
    aufgezählt. Weil Präferenz und Alternative unabhängig gezogen werden und der Best-Path-F1
    das Maximum über beide ist, gilt pro Wunde
        E[F1] = E[max(U, V)],
    wobei U (bzw. V) der beste F1 eines zufälligen Präferenz- (bzw. Alternativ-)Sets gegen die
    Präferenz oder Alternative des Experten ist. U und V werden über alle Kombinationen exakt
    bestimmt.

Majority-Baseline (Leave-One-Out)
    Für jede Wunde wird die häufigste Präferenzkombination des jeweiligen Experten in den
    übrigen Wunden bestimmt (Leave-One-Out) und als Vorhersage verwendet – ohne Alternative.
    Gezählt werden vollständige Sets (z. B. {Solvaline N, Suprasorb X + PHMB}), nicht einzelne
    Produkte. Dadurch ist die Vorhersage immer eine Kombination, die der Experte tatsächlich
    gewählt hat, und die Anzahl der Produkte ergibt sich aus den Daten (nicht fest vorgegeben).
    Auf Level 2/3 werden die Sets vor dem Zählen auf Familien bzw. Klassen gemappt.
    Gleichstand: alphabetisch nach Produktnamen (deterministisch).

Ausschluss: Wunden, an denen der jeweilige Experte weder Präferenz noch Alternative angegeben
hat, werden nicht bewertet (n = 57 für Experte 1, n = 58 für Experte 2).
"""

import os
import itertools
from collections import Counter

import numpy as np
import pandas as pd

from primaerverband_calc import (
    BASE_DIR, GT1_PATH, GT2_PATH, TWO_PATH, IMAGE_IDS,
    safe_parse_set, set_f1, best_path_f1, map_level_2, map_level_3,
)

CATALOG_PATH = os.path.join(BASE_DIR, "data", "l&r_produktkatalog", "lr1_produktkatalog.md")
EXPERT_GT_PATHS = {1: GT1_PATH, 2: GT2_PATH}
LEVEL_MAPS = {1: set, 2: map_level_2, 3: map_level_3}


def load_catalog_products(path: str = CATALOG_PATH) -> list[str]:
    """Alle Primärverbände des L&R-Katalogs (Überschriften der Ebene ###)."""
    with open(path, encoding="utf-8") as f:
        return [line[4:].strip() for line in f if line.startswith("### ")]


def load_expert_sets(expert_id: int) -> dict:
    """{image_id: (Präferenz-Set, Alternativ-Set)} aus der normalisierten Ground Truth."""
    df = pd.read_csv(EXPERT_GT_PATHS[expert_id], sep=";")
    return {r.image_id: (safe_parse_set(r.praeferenz_produkt), safe_parse_set(r.alternative_produkt))
            for _, r in df.iterrows()}


def load_ki_sets(path: str = TWO_PATH) -> dict:
    """{image_id: (Präferenz-Set, Alternativ-Set)} aus einer normalisierten KI-CSV."""
    df = pd.read_csv(path)
    return {r.image_id: (safe_parse_set(r.praeferenz_wundauflage), safe_parse_set(r.alternativ_wundauflage))
            for _, r in df.iterrows()}


def evaluable_wounds(expert_sets: dict) -> list[str]:
    """Wunden, an denen der Experte mindestens eine Empfehlung abgegeben hat."""
    return [w for w in IMAGE_IDS if w in expert_sets and (expert_sets[w][0] or expert_sets[w][1])]


def _best_f1_of_all_sets(k: int, gt_pref: set, gt_alt: set, products: list[str], mapper) -> np.ndarray:
    """F1 jedes möglichen k-Sets gegen das jeweils besser passende Experten-Set (Präferenz oder Alternative)."""
    gt_sets = [mapper(gt_pref)] + ([mapper(gt_alt)] if gt_alt else [])
    return np.array([max(set_f1(mapper(set(combo)), g) for g in gt_sets)
                     for combo in itertools.combinations(products, k)])


def _expected_max(u: np.ndarray, v: np.ndarray | None) -> float:
    """Exakter Erwartungswert von max(U, V) für unabhängige, gleichverteilte U und V."""
    if v is None:
        return float(u.mean())
    v_sorted = np.sort(v)
    cumsum = np.concatenate([[0.0], np.cumsum(v_sorted)])
    idx = np.searchsorted(v_sorted, u, side="right")          # Anzahl V <= u
    return float(np.mean((idx * u + (cumsum[-1] - cumsum[idx])) / len(v_sorted)))


def random_baseline_exact(expert_id: int, level: int = 1, size_source: str = TWO_PATH) -> dict:
    """
    Exakter Erwartungswert der Random-Baseline (siehe Modul-Docstring).
    size_source: KI-CSV, aus der die Set-Größen pro Wunde übernommen werden.
    Rückgabe: {"f1": Mittelwert in %, "n": Anzahl Wunden, "per_wound": {image_id: F1}}
    """
    products = load_catalog_products()
    expert = load_expert_sets(expert_id)
    ki = load_ki_sets(size_source)
    mapper = LEVEL_MAPS[level]
    per_wound = {}
    for w in evaluable_wounds(expert):
        k_pref, k_alt = len(ki[w][0]), len(ki[w][1])
        gt_pref, gt_alt = expert[w]
        u = _best_f1_of_all_sets(k_pref, gt_pref, gt_alt, products, mapper)
        v = _best_f1_of_all_sets(k_alt, gt_pref, gt_alt, products, mapper) if k_alt else None
        per_wound[w] = _expected_max(u, v)
    return {"f1": 100 * np.mean(list(per_wound.values())), "n": len(per_wound), "per_wound": per_wound}


def majority_baseline_loo(expert_id: int, level: int = 1) -> dict:
    """
    Majority-Baseline mit Leave-One-Out (siehe Modul-Docstring).
    Rückgabe: {"f1": Mittelwert in %, "n": Anzahl Wunden, "per_wound": {image_id: F1},
               "gewaehlt": Counter der vorhergesagten Kombinationen}
    """
    expert = load_expert_sets(expert_id)
    mapper = LEVEL_MAPS[level]
    wounds = evaluable_wounds(expert)
    per_wound, chosen = {}, Counter()
    for w in wounds:
        counts = Counter(frozenset(mapper(expert[v][0])) for v in wounds if v != w and expert[v][0])
        prediction = set(sorted(counts.items(), key=lambda kv: (-kv[1], sorted(kv[0])))[0][0])
        chosen[" + ".join(sorted(prediction))] += 1
        per_wound[w] = best_path_f1(prediction, set(), mapper(expert[w][0]), mapper(expert[w][1]))
    return {"f1": 100 * np.mean(list(per_wound.values())), "n": len(per_wound),
            "per_wound": per_wound, "gewaehlt": chosen}


def compute_baseline_table(levels=(1, 2)) -> pd.DataFrame:
    """Random- und Majority-Baseline pro Experte und Level als Tabelle (F1 in %)."""
    rows = []
    for level in levels:
        for expert_id in (1, 2):
            rnd = random_baseline_exact(expert_id, level)
            maj = majority_baseline_loo(expert_id, level)
            rows.append({"Level": level, "Experte": expert_id, "n": rnd["n"],
                         "Random": round(rnd["f1"], 1), "Majority (LOO)": round(maj["f1"], 1),
                         "Majority-Vorhersage": ", ".join(maj["gewaehlt"])})
    return pd.DataFrame(rows)
