# Anhang B: Medizinisches Normalisierungsschema (Mapping-Übersicht)

## B.1 Methodischer Überblick

Zur objektivierten Evaluation der Sprachmodell-Generierungen (GPT-5) gegenüber den Experten-Ground-Truths (Lohmann & Rauscher sowie NursIT) wurden die freien Textangaben und synonymen Bezeichnungen über ein regelbasiertes Normalisierungsschema auf diskrete Zielkategorien gemappt. Dies gewährleistet ein konsistentes Set-F1- und Exact-Match-Evaluating über alle 60 Wundfälle.

Das vollständige Mappings-Register umfasst insgesamt **1.564 Einzelregeln**. Um den gedruckten Umfang der Arbeit angemessen zu halten, zeigt die folgende Übersichtstabelle die Struktur aller Mapping-Module sowie repräsentative Beispiele. Das vollständige tabellarische Register ist der Arbeit im digitalen Anhang (`anhang_mappings.csv`) beigefügt.


## B.2 Übersicht der Mapping-Module

| Quelle | Kategorie / Modul | Anzahl Regeln | Repräsentative Beispiel-Eingaben |
| :--- | :--- | :---: | :--- |
| `mappings.py` | `ANTIMIKROBIELL_GT_MAPPING` | 6 | `Silber (Ag⁺)`, `Silber (Ag+)`, `PHMB` |
| `mappings.py` | `DEBRIDEMENT_GT_MAPPING` | 23 | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)`, `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `mappings.py` | `EXSUDAT_GT_MAPPING` | 62 | `Annahme stark`, `Große Wunde: stark, da Mazerationen am Wundrand
Kleine Nekrose: trocken`, `Keine` |
| `mappings.py` | `HAUTSCHUTZ_GT_MAPPING` | 4 | `Hautschutzfilm / Barrierespray`, `Zinksalbe / Zinkpaste`, `Wundrandschutzpaste` |
| `mappings.py` | `KOMPRESSION_GT_MAPPING` | 5 | `Mehrkomponentensysteme (2-/4-Lagen)`, `Kurzzugbinden`, `Adaptive Kompressionsbandagen (Wrap)` |
| `mappings.py` | `LOKALISATION_GT_MAPPING` | 134 | `...stark exsudierendes, nekrotisch belegtes Ulcus mit grünlicher Verfärbung typisch für Pseudomonas aeruginosa.`, `?`, `???` |
| `mappings.py` | `LOKALISATION_KEYWORDS` | 6 | `Fuß`, `Bein`, `Arm` |
| `mappings.py` | `PRODUKT_GT_MAPPING` | 43 | `Schaumstoffverbände (Foam)`, `Schaumstoffverbände`, `Hydrofaser / Hydrofiber` |
| `mappings.py` | `SEKUNDAERVERBAND_GT_MAPPING` | 53 | `Schaumstoffverbände (Foam)`, `Schaumstoffverbände`, `Schaumverband` |
| `mappings.py` | `SPELLING_MAPPING` | 2 | `ulcus`, `decubitus` |
| `mappings.py` | `SPUELLOESUNG_GT_MAPPING` | 10 | `Neutrale Spüllösung (NaCl 0,9 % / Ringer-Lösung)`, `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)`, `Neutrale Spüllösung (NaCl, Ringer)` |
| `mappings.py` | `WUNDRAND_GT_MAPPING` | 33 | `["Epibolie (eingerollter Wundrand)","Gerötet / entzündlich","Mazeriert"]`, `["Epibolie (eingerollter Wundrand)","Gerötet / entzündlich"]`, `["Epibolie (eingerollter Wundrand)","Mazeriert"]` |
| `mappings.py` | `WUNDTYP_GT_MAPPING` | 143 | `Ausgedehnte feuchte Nekrose`, `Ausgetrtenes Blut oder Lymphe aus den entsprechenden Gefäßen mit Verteilung an der betroffenen Extremität`, `Dekubitus` |
| `mappings.py` | `WUNDUMGEBUNG_GT_MAPPING` | 38 | `["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)","Erythem / Rötung"]`, `["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]`, `["Ekzem / Dermatitis","Erythem / Rötung"]` |
| `mappings_LR.py` | `DEBRIDEMENT_GT_MAPPING` | 6 | `Autolytisches Debridement`, `Chirurgisches Debridement`, `Debrisoft Duo` |
| `mappings_LR.py` | `EXSUDAT_GT_MAPPING` | 62 | `Annahme stark`, `Große Wunde: stark, da Mazerationen am Wundrand
Kleine Nekrose: trocken`, `Keine` |
| `mappings_LR.py` | `LOKALISATION_GT_MAPPING` | 134 | `...stark exsudierendes, nekrotisch belegtes Ulcus mit grünlicher Verfärbung typisch für Pseudomonas aeruginosa.`, `?`, `???` |
| `mappings_LR.py` | `LOKALISATION_KEYWORDS` | 10 | `Abdomen`, `Fuß`, `Bein` |
| `mappings_LR.py` | `PRODUKT_GT_MAPPING` | 95 | `Actico UlcerSys System`, `ReadyWrap Untere Extremität`, `Rosidal TCS` |
| `mappings_LR.py` | `WUNDGRUND_GT_MAPPING` | 266 | `nekrotisch`, `Fibrinbelegt`, `Sauber, bis auf die aufgetragene Salbe` |
| `mappings_LR.py` | `WUNDRAND_GT_MAPPING` | 33 | `["Epibolie (eingerollter Wundrand)","Gerötet / entzündlich","Mazeriert"]`, `["Epibolie (eingerollter Wundrand)","Gerötet / entzündlich"]`, `["Epibolie (eingerollter Wundrand)","Mazeriert"]` |
| `mappings_LR.py` | `WUNDTYP_GT_MAPPING` | 143 | `Ausgedehnte feuchte Nekrose`, `Ausgetrtenes Blut oder Lymphe aus den entsprechenden Gefäßen mit Verteilung an der betroffenen Extremität`, `Dekubitus` |
| `mappings_LR.py` | `WUNDUMGEBUNG_GT_MAPPING` | 38 | `["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)","Erythem / Rötung"]`, `["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]`, `["Ekzem / Dermatitis","Erythem / Rötung"]` |

## B.3 Repräsentative Auszüge wichtiger Zielkategorien

### Auszug 1: Exsudat-Mengen-Mapping (`EXSUDAT_GT_MAPPING`)

| Rohbegriff / Freitext | Normalisierter Zielbegriff |
| :--- | :--- |
| `Annahme stark` | `Stark` |
| `Große Wunde: stark, da Mazerationen am Wundrand
Kleine Nekrose: trocken` | `Stark` |
| `Keine` | `Keine` |
| `Leicht` | `Leicht` |
| `Mässig` | `Mäßig` |
| `Mäßig` | `Mäßig` |
| `Nekrosen: kein Exsudat. Unterschenkel mäßig` | `Mäßig` |
| `Stark` | `Stark` |

### Auszug 2: Primärverband Produkt-Mapping (`PRODUKT_GT_MAPPING`)

| Rohbegriff / Handelsname | Normalisierter Zielbegriff |
| :--- | :--- |
| `Schaumstoffverbände (Foam)` | `Schaumstoffverbände (Foam)` |
| `Schaumstoffverbände` | `Schaumstoffverbände (Foam)` |
| `Hydrofaser / Hydrofiber` | `Hydrofaser / Hydrofiber` |
| `Alginate` | `Alginate` |
| `Hydrogele (Kompresse)` | `Hydrogele (Kompresse)` |
| `Hydrokolloide` | `Hydrokolloide` |
| `Superabsorber` | `Superabsorber` |
| `Wundkontaktschichten (Silikon/Paraffin)` | `Wundkontaktschichten (Silikon/Paraffin)` |
| `Lipidokolloid-Auflagen` | `Wundkontaktschichten (Silikon/Paraffin)` |
| `Hydropolymerverbände` | `Schaumstoffverbände (Foam)` |