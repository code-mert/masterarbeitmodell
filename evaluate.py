import logging
import pprint
import pandas as pd
from eval.loaders import load_ground_truth, load_llm_outputs, matched_image_ids
from eval.mapping import align
from eval.normalize import to_set
from eval.metrics import set_f1, exact_match, best_path_f1

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def verify_pipeline():
    csv_path = "data/ground_truth/allgemeine_verbandsklassen.csv"
    json_dir = "runs/gpt-5/zero_shot"
    
    print("=" * 80)
    print("LADE DATEN...")
    print("=" * 80)
    
    # 1. Load Ground Truth
    gt_data = load_ground_truth(csv_path)
    n_finished_gt = sum(1 for rec in gt_data.values() if rec.get("ist_fertig") in (True, "true", "True"))
    
    # 2. Load LLM Outputs
    llm_data = load_llm_outputs(json_dir)
    
    # 3. Match Image IDs
    matched_ids = matched_image_ids(gt_data, llm_data)
    
    print("\n" + "=" * 80)
    print("STATISTIKEN")
    print("=" * 80)
    print(f"Einträge in Ground Truth (gesamt): {len(gt_data)}")
    print(f"Davon 'ist_fertig' markiert:       {n_finished_gt}")
    print(f"Geladene LLM-Outputs:              {len(llm_data)}")
    print(f"Größe der Schnittmenge (Match):    {len(matched_ids)}")
    print("=" * 80)
    
    if len(matched_ids) > 0:
        results = []
        for img_id in matched_ids:
            gt_rec = gt_data[img_id]
            llm_rec = llm_data[img_id]
            
            # Phase 1: Strukturangleichung
            aligned = align(gt_rec, llm_rec)
            
            # Phase 2: Stufe 1 (Roh-Normierung)
            # 1. Primaerverband (Best-Path)
            llm_praef = to_set(aligned["primaerverband"]["llm_praef"])
            llm_alt = to_set(aligned["primaerverband"]["llm_alt"])
            gt_praef = to_set(aligned["primaerverband"]["gt_praef"])
            gt_alt = to_set(aligned["primaerverband"]["gt_alt"])
            
            prim_f1, prim_exact, _, _ = best_path_f1(llm_praef, llm_alt, gt_praef, gt_alt)
            
            row = {
                "image_id": img_id,
                "primaerverband_f1": prim_f1,
                "primaerverband_exact": float(prim_exact)
            }
            
            # 5 weitere Ebenen
            for level in ["debridement", "antimikrobielles_agens", "sekundaerverband", "hautschutz", "kompression"]:
                llm_set = to_set(aligned[level]["llm"])
                gt_set = to_set(aligned[level]["gt"])
                
                f1 = set_f1(llm_set, gt_set)
                exact = exact_match(llm_set, gt_set)
                
                row[f"{level}_f1"] = f1
                row[f"{level}_exact"] = float(exact)
                
            results.append(row)
            
        df_results = pd.DataFrame(results)
        df_results = df_results.sort_values("image_id").reset_index(drop=True)
        
        print("\n" + "=" * 80)
        print("PHASE 2 - ERGEBNISSE PRO BILD")
        print("=" * 80)
        print(df_results.to_string(index=False))
        print("=" * 80)
        
        # Aggregat-Tabelle
        summary_data = []
        levels = ["primaerverband", "debridement", "antimikrobielles_agens", "sekundaerverband", "hautschutz", "kompression"]
        
        for level in levels:
            mean_f1 = df_results[f"{level}_f1"].mean()
            exact_rate = df_results[f"{level}_exact"].mean()
            
            summary_data.append({
                "Ebene": level,
                "F1-Score (Mean)": mean_f1,
                "Exact-Match-Rate": exact_rate
            })
            
        df_summary = pd.DataFrame(summary_data)
        print("\n" + "=" * 80)
        print("AGGREGAT-TABELLE (MITTELWERTE)")
        print("=" * 80)
        print(df_summary.to_string(index=False))
        print("=" * 80)
        
        # Show alignment sample for wunde_01
        sample_id = matched_ids[0]
        print("\n" + "=" * 80)
        print(f"PHASE 1 & 2 SAMPLE ALIGNMENT & SETS (Beispiel: {sample_id})")
        print("=" * 80)
        aligned = align(gt_data[sample_id], llm_data[sample_id])
        print("PRIMAERVERBAND:")
        print(f"  LLM sets: {to_set(aligned['primaerverband']['llm_praef'])}, {to_set(aligned['primaerverband']['llm_alt'])}")
        print(f"  GT sets:  {to_set(aligned['primaerverband']['gt_praef'])}, {to_set(aligned['primaerverband']['gt_alt'])}")
        for level in ["debridement", "antimikrobielles_agens", "sekundaerverband", "hautschutz", "kompression"]:
            print(f"{level.upper()}:")
            print(f"  LLM set: {to_set(aligned[level]['llm'])}")
            print(f"  GT set:  {to_set(aligned[level]['gt'])}")
        print("=" * 80)
    else:
        print("\nKeine gematchten Bild-IDs für die Auswertung vorhanden.")

if __name__ == "__main__":
    verify_pipeline()