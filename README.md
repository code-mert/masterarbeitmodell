# Wundbild-Analyse & Verbandmittelempfehlung via LLMs

Dieses Repository enthält die Vergleiche, Evaluationen und Pipelines zur KI-gestützten Wundbild-Analyse und automatisierten Verbandmittelempfehlung (auf Basis generischer Verbandklassen sowie des Lohmann & Rauscher Produktkatalogs).

Das Projekt evaluiert verschiedene Prompting-Strategien (Zero-Shot, Few-Shot, 2-Stage Chain-of-Thought) mit multimodalen KI-Modellen (z. B. GPT-4o / GPT-5) und vergleicht die Modellergebnisse systematisch mit Experten-Ground-Truth-Daten.

---

## 📁 Ordnerstruktur & Übersicht – Wo findet man was?

| Ordner / Datei | Beschreibung |
| :--- | :--- |
| **`data/`** | Enthält alle Eingabedaten:<br>• `ground_truth/`: CSV- und Annotationsdateien der Experten-Annotationen.<br>• `wundbilder/`: Bilddateien der evaluierten Wunden.<br>• `produktkatalog/` & `l&r_produktkatalog/`: Markdown- und Katalogbeschreibungen für Verbandmittel.<br>• `llm_outputs/`: Gesammelte LLM-Ergebnisse. |
| **`exports/`** | Enthält exportierte Auswertungen & Berichte:<br>• Ground Truth & Vergleiche als Excel (`NursIT_Allgemeine_Verbandsklassen.xlsx`, `Lohmann_Rauscher_Vergleich_Experten_KI.xlsx`, `Wundtyp_Vergleich_Experten_KI.xlsx`, etc.).<br>• Anhang-Mapping-Tabellen in CSV, JSON, Markdown und LaTeX (`anhang_mappings.*`).<br>• Generierte Heatmaps und Plots zur F1- und Exact-Match-Auswertung. |
| **`notebooks/`** | Jupyter Notebooks für Datenanalyse und Visualisierung:<br>• `analyse.ipynb` & `analyse_3prompts.ipynb`: Hauptanalyse-Notebooks.<br>• `analyse_categories/`: Detail-Analysen pro Wundkategorie (Wundtyp, Lokalisation, Exsudat, Wundrand, etc.).<br>• `analyse_lr/`, `analyse_lr_2stage/`, `analyse_lr_fewshot/`: Spezifische Auswertungen für den Lohmann & Rauscher Produktkatalog.<br>• Enthält die Daten-Normalisierung, F1-Score- und Exact-Match-Berechnungen. |
| **`prompts/`** | Die Prompting-Strategien & System-Prompts für das KI-Modell:<br>• `zero_shot_prompt.py`: Direkte Wundbild-Analyse ohne Vorab-Beispiele.<br>• `few_shot_prompt.py`: Analyse mit integrierten Referenzbeispielen.<br>• `two_stage_prompt.py`: Zweistufiger Chain-of-Thought-Ansatz. |
| **`runs/`** | Speichert die Roh-JSON-Antworten der KI-Modell-Experimente (z. B. strukturierte Antworten von GPT-5 / GPT-4o für Zero-Shot, Few-Shot und 2-Stage). |
| **`schema.py`** | Definiert das allgemeine JSON/Pydantic Output-Schema für die strukturierten KI-Antworten (Wundkategorien & generische Verbandklassen). |
| **`lr_schema.py`** | Definiert das spezialisierte Output-Schema für Empfehlungen aus dem Lohmann & Rauscher Produktkatalog. |
| **`run_experiment.py`** | Hauptskript zur Durchführung der KI-Experimente. Ermöglicht die interaktive Auswahl von Prompt-Ansatz und Produktkatalog, führt die API-Aufrufe durch und speichert die JSON-Outputs in `runs/`. |
| **`evaluate.py`** | Skript zur schnellen Konsolen-Evaluierung und Überprüfung der Daten-Pipeline. |
| **`eval/`** | Python-Paket mit Evaluierungslogik:<br>• `metrics.py`: F1-Score, Exact-Match und Best-Path-F1 Metriken.<br>• `normalize.py`: Normalisierung von Textfeldern und Freitexten.<br>• `mapping.py`: Angleichung von Ground-Truth- und LLM-Datenstrukturen.<br>• `loaders.py`: Laderoutinen für CSV, JSON und Bild-IDs. |
| **`core/`** | Kernfunktionen wie `storage.py` zur sicheren Speicherung von Läufen und Hash-Berechnung. |

---

## 🚀 Schnelleinstieg & Installation

### 1. Repository klonen & Umgebung einrichten

```bash
git clone <repository-url>
cd Modell

# Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate  # Unter Windows: .venv\Scripts\activate

# Abhängigkeiten installieren (falls requirements.txt vorhanden)
pip install -r requirements.txt
```

### 2. Umgebungsvariablen konfigurieren

Erstelle eine `.env`-Datei im Wurzelverzeichnis des Projekts und trage deinen OpenAI API-Schlüssel ein:

```env
OPENAI_API_KEY=dein_openai_api_key_hier
```

---

## 🧪 Experimente ausführen (`run_experiment.py`)

Um ein neues Experiment mit den Wundbildern durchzuführen:

```bash
python run_experiment.py
```

Das Skript führt dich durch ein interaktives Menü zur Auswahl des Prompt-Ansatzes und des Katalogs:
1. **Zero-Shot** (Generischer Produktkatalog)
2. **Zero-Shot** (Lohmann & Rauscher Katalog)
3. **Few-Shot** (Lohmann & Rauscher Katalog)
4. **Few-Shot** (Generischer Produktkatalog)
5. **2-Stage CoT** (Lohmann & Rauscher Katalog)
6. **2-Stage CoT** (Generischer Produktkatalog)

Die Ergebnisse werden automatisch im Ordner `runs/` als JSON-Dateien abgelegt.

---

## 📊 Evaluation & Analysen (`evaluate.py` & `notebooks/`)

### Schnellauswertung per Konsole
```bash
python evaluate.py
```

### Detaillierte Notebook-Analysen
Öffne Jupyter Lab / Notebook, um die Auswertungsnotebooks im Ordner `notebooks/` zu starten:

```bash
jupyter lab
```

Empfohlener Einstieg:
- `notebooks/analyse.ipynb`: Gesamtauswertung der F1-Scores und Exact-Match-Raten.
- `notebooks/analyse_categories/`: Detaillierte Einzelanalysen pro Wundmerkmal.

---

## 📄 Lizenz & Hinweis

Dieses Repository entstand im Rahmen einer wissenschaftlichen Arbeit zur Evaluation von Multimodalen Großen Sprachmodellen (LLMs) in der klinischen Wundbeurteilung.
