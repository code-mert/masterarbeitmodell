"""
Medizinisches Mapping-Regelwerk für Wundtypen (Version 8 - Audit-Sicher).

WISSERNSCHAFTLICHES REGELWERK (Label-Blind & Textbasiert):

1. HÖCHSTE PRIORITÄT - Enthaltungen & Meta-Verweise:
   - Verweigerungen ("nehme keine Beurteilung vor") mappen zu "Enthaltung / keine Angabe".
   - Meta-Verweise ("gleiche Beurteilung wie Wunde 53") werden aufgelöst zu "Dekubitus".

2. DIFFERENTIALDIAGNOSEN & UNKLARHEIT (DD-Regel):
   - Wenn im Text 2 oder mehr gleichrangige Ätiologien genannt werden ("oder", "DD", "könnte sein", "ebenso möglich"),
     oder die Ursache explizit als unklar beschrieben wird ("Genese unklar", "Ätiologie nicht sicher", "Prüfung erforderlich"),
     mappt der Befund konsequent zu "Ulkus (Ätiologie unspezifisch)".

3. POSTOPERATIVE WUNDEN & DEHISZENZEN:
   - OP-Wunden, Platzbauch, Dehiszenzen, Spalthautentnahmestellen und Wunden nach Meshgraft mappen zu "Postoperative Wunde / Dehiszenz".

4. DIABETISCHES FUSSSYNDROM (DFS):
   - Erfordert die explizite Bestätigung von "diabetisch", "neuropathisch" oder "DFS" im Text ohne widersprüchliche DD-Mehrfachnennungen.

5. DEKUBITUS (Reine Text-Regel):
   - Alle druckbedingten Geschwüre ("Dekubitus", "Druckulcus", "Druckgeschwür", "EPUAP", "Fersendekubitus") mappen rein textbasiert zu "Dekubitus".
   - Beseitigung jeglicher Ground-Truth-Leakage!

6. VERBRENNUNGSWUNDEN:
   - Thermische Schädigungen, Verbrennungen, Verbrühungen und thermisch-traumatische Kombinationen mappen zu "Verbrennungswunde".

7. TRAUMATISCHE WUNDEN (Strikte Abgrenzung):
   - Erfordert explizite akute Traumata, Unfälle, Schnitte, Stiche oder Insektenstiche.
   - Nicht-traumatische Sonderfälle (Vaskulitis, Hämangiom, Abszess, Extravasation, Pilonidalsinus) werden NICHT erzwungen gemappt, sondern verbleiben als ungemappter Freitext.

8. UNSPEZIPHISCHE ULZERA:
   - Allgemeine Geschwüre ("Ulcus", "Ulkus", "Ulzeration") ohne nachgewiesene Ätiologie mappen zu "Ulkus (Ätiologie unspezifisch)".
"""

EXPLICIT_WUNDTYP_RULES = {
    # -------------------------------------------------------------
    # 1. ENTHALTUNG / META-VERWEISE
    # -------------------------------------------------------------
    "Hämangiom ist ein Spezialgebiet. In der Regel ist dieses innerhalb des ersten Lebensjahres rückläufig. Deshalb nehme ich hier keine Beurteilung vor.": "Enthaltung / keine Angabe",
    "gleiche Beurteilung wie Wunde 53": "Dekubitus",
    "keine Angabe": "Enthaltung / keine Angabe",
    "?": "Enthaltung / keine Angabe",
    "???": "Enthaltung / keine Angabe",
    "Sonstiges": "Enthaltung / keine Angabe",

    # -------------------------------------------------------------
    # 2. USER REFINEMENTS (Spezifische Nutzer-Anpassungen)
    # -------------------------------------------------------------
    # Traumatische/thermische Hautläsion -> Verbrennungswunde
    "Traumatische/thermische Hautläsion mit ausgedehnter Nekrose": "Verbrennungswunde",

    # Neuropathischer diabetischer Ulcus -> DFS
    "könnte diabetischer ulcus sein auf grund einer neuropathie": "Diabetisches Fußsyndrom (DFS)",

    # Ulcus bei vermutetem Diabetes -> Ulkus (Ätiologie unspezifisch)
    "Ulcus, bei vermutetem Diabetes": "Ulkus (Ätiologie unspezifisch)",

    # -------------------------------------------------------------
    # 3. DIFFERENTIALDIAGNOSEN & UNKLARE ÄTIOLOGIEN -> Ulkus (Ätiologie unspezifisch)
    # -------------------------------------------------------------
    "Dekubitus, Diabetisches Fußulkus (infiziertes neuropathisches Ulkus)": "Ulkus (Ätiologie unspezifisch)",
    "Dekubitus, Diabetisches Fußulkus": "Ulkus (Ätiologie unspezifisch)",
    "chronisches Ulkus (DD venös / posttraumatisch / sekundär heilend)": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus unklarer Genese, könnte diabet. Ulcus sein, möglich ebenso traumatologisch": "Ulkus (Ätiologie unspezifisch)",
    "könnte ein diabetischer Fuß sein … traumatologische Indikation ebenso nicht ausgeschlossen": "Ulkus (Ätiologie unspezifisch)",
    "könnte arterieller Ulcus oder diabetischer Ulcus ( Angiopathie) auf Grund der Mangeldurchblutung  sein.": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus unklarer Genese, könnte diabet. Ulcus sein, möglich ebenso traumatologisch": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus. Ursache klären sollte es ein diabet. Fuß sein dann Prüfung ob angiopathisch oder neuropathisch,\nDruckentlastung und Ursachenbeseitigung.": "Ulkus (Ätiologie unspezifisch)",
    "Ulcera rechter Fuß. könnte ursächlich diabetischer Fuß sein ( Neuropathie, Angiopathie) oder arterielles ulcus schäden auf Grund fehlender Durchblutung": "Ulkus (Ätiologie unspezifisch)",
    "Sekundär heilende, oberflächliche Wunde mit Fibrinbelag (unklare Genese, z. B. posttraumatisch/ulzerierend)": "Ulkus (Ätiologie unspezifisch)",
    "Traumatische/chronische Wunde (Fußulkus unklarer Genese)": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus unklarer Genese, könnte Venös oder arteriell oder mixum sein.\nBeachte kleine Nekrose an der Ferse plantar": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus, durch die Mangelernährung ( keine Durchblutung) im Wundgebiet  könnte es sich um einen Dekubitus oder ulcus cruris handeln.": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus auf Grund von Mangelernährung des Gewebes, Druckschäden in Kombination mit Gefäßschäden": "Ulkus (Ätiologie unspezifisch)",
    "Gravitationsulzera/Druckulzera": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus cruris möglich arteriell oder mixtum": "Ulkus (Ätiologie unspezifisch)",
    "Ulkus am Unterschenkel (Ätiologie unklar, Bild legt venöses Ulkus nahe)": "Ulkus (Ätiologie unspezifisch)",
    "Mehrere Ulzera am Fuß; Ätiologie im Bild nicht sicher (druck-/ischämisch möglich)": "Ulkus (Ätiologie unspezifisch)",
    "Mehrere nekrotisch-belegte Ulzera am Fuß (druck-/ischämieassoziiert möglich)": "Ulkus (Ätiologie unspezifisch)",
    "Nekrotische Ulzeration (unklare Genese, möglich druck-/ischämiebedingt)": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus cruris (bildbasiert; Ätiologie nicht sicher)": "Ulkus (Ätiologie unspezifisch)",
    "Ulcus cruris (Verdacht anhand Bild)": "Ulkus (Ätiologie unspezifisch)",

    # -------------------------------------------------------------
    # 4. POSTOPERATIVE WUNDE / DEHISZENZ
    # -------------------------------------------------------------
    "Postoperative Wunde": "Postoperative Wunde / Dehiszenz",
    "Postoperative Wunde abdominal": "Postoperative Wunde / Dehiszenz",
    "Postoperative Wunddehiszenz": "Postoperative Wunde / Dehiszenz",
    "Postoperative Wunddehiszenz, infiziert": "Postoperative Wunde / Dehiszenz",
    "Postoperative Wunde (Wunddehiszenz) nahe Stoma": "Postoperative Wunde / Dehiszenz",
    "Postoperative Wunde (Wunddehiszenz), parastomal": "Postoperative Wunde / Dehiszenz",
    "Postoperative Wunde (Spalthautentnahmestelle)": "Postoperative Wunde / Dehiszenz",
    "Postoperative Wunde (dehiszient, sekundär heilend)": "Postoperative Wunde / Dehiszenz",
    "Postoperative/traumatische sekundär heilende Wunde": "Postoperative Wunde / Dehiszenz",
    "Platzbauch": "Postoperative Wunde / Dehiszenz",
    "Platzbauch nach möglichem chirurgischem Eingriff": "Postoperative Wunde / Dehiszenz",
    "Dehiszente Operationswunde": "Postoperative Wunde / Dehiszenz",
    "Ulcus nach Meshgraft (zumindest lässt die Struktur darauf schließen), eventuell ist die Struktur aber einer Unterdrucktherapie geschuldet": "Postoperative Wunde / Dehiszenz",

    # -------------------------------------------------------------
    # 5. DEKUBITUS
    # -------------------------------------------------------------
    "Dekubitus": "Dekubitus",
    "Decubitus": "Dekubitus",
    "Dekubtis": "Dekubitus",
    "Dekubitalulkus": "Dekubitus",
    "Fersendekubitus": "Dekubitus",
    "nekrotischer Defekt / Dekubitus": "Dekubitus",
    "nekrotischer Dekubitus li Ferse": "Dekubitus",
    "Dekubitus, vermutlich am Außenknöchel": "Dekubitus",
    "Dekubitus an der Ferse": "Dekubitus",
    "Dekubitus mit Nekrose": "Dekubitus",
    "tiefer Dekubitus": "Dekubitus",
    "Dekubitus mit Taschenbildung": "Dekubitus",
    "Dekubtis im Sakralbereich, großflächig": "Dekubitus",
    "oberflächlicher Dekubitus ( 2 Stück)": "Dekubitus",
    "Ulcus decubitus": "Dekubitus",
    "massives Ulcus dekubitus": "Dekubitus",
    "Ulcus Dekubitus": "Dekubitus",
    "Ulcus dekubitus": "Dekubitus",
    "Ulkus an der Ferse, warsch. Dekubitus nach EPUAP  Stadium 3": "Dekubitus",
    "Ulcus Dekubitus nach Epuap Grad 2 bis 3": "Dekubitus",
    "Ulcus dekubitus Ferse,  Stadium 3 / 4": "Dekubitus",
    "Ulcus decubitus Nach Epuap Grad 2 bis 3": "Dekubitus",
    "Dekubitus sacralbereich": "Dekubitus",
    "Dekubitus epuap Stadium 3 / 4": "Dekubitus",
    "Ulcus Dekubitus Epuap Grad 3 / 4": "Dekubitus",
    "Dekubitus Grad 2 oder 3 nach EPUAP.\nNicht genau zu definieren, ob sich Unterminierungen vorhanden sind.": "Dekubitus",
    "Ulkus Dekubitus am Os sacrum  nach Epuap Grad 2 / 3": "Dekubitus",
    "Ulcus Dekubitus Bereich OS Sacrum": "Dekubitus",
    "Dekubitalulkus (Druckulcus) Ferse": "Dekubitus",
    "Dekubitalulkus (Druckulcus) an der Ferse": "Dekubitus",
    "Dekubitalulkus (Druckulkus)": "Dekubitus",
    "Dekubitalulkus (Druckulkus) an der Ferse": "Dekubitus",
    "Dekubitalulkus (Ferse)": "Dekubitus",
    "Dekubitus (Druckulkus)": "Dekubitus",
    "Dekubitus (Druckulkus) Ferse": "Dekubitus",
    "Dekubitus (Druckulkus) der Ferse": "Dekubitus",
    "Dekubitus (Druckulzera)": "Dekubitus",
    "Dekubitus (Fersenulkus)": "Dekubitus",
    "Dekubitus (druckbedingtes Ulkus) an der Ferse": "Dekubitus",
    "Druckulzer (Ferse/Fußulkus)": "Dekubitus",
    "Druckulcus (Dekubitus)": "Dekubitus",
    "Druckulcus (Ferse)": "Dekubitus",
    "Druckulcus an der Ferse": "Dekubitus",
    "Druckulcus der Ferse (Fersendekubitus) mit trockener Eschar": "Dekubitus",
    "Druckulkus / Ulkus an der Ferse": "Dekubitus",
    "Druckulkus der Ferse (Fersenulkus)": "Dekubitus",
    "Druckulzeration / Fersenulkus": "Dekubitus",
    "Dekubitus (Druckulcus an der Ferse)": "Dekubitus",
    "Dekubitus (Druckulcus)": "Dekubitus",
    "Dekubitus (Druckulkus der Ferse)": "Dekubitus",
    "Dekubitus (Fersendruckulkus)": "Dekubitus",
    "Dekubitus (mehrere Ulzera)": "Dekubitus",
    "Dekubitus (sakral/paraglutäal)": "Dekubitus",
    "Druckulcus (Zehenulkus)": "Dekubitus",
    "Druckulcus am Fuß (mehrere Ulzera)": "Dekubitus",

    # -------------------------------------------------------------
    # 6. DIABETISCHES FUSSSYNDROM (DFS)
    # -------------------------------------------------------------
    "Diabetisches Fußulkus": "Diabetisches Fußsyndrom (DFS)",
    "Diabetisches Fußsyndrom": "Diabetisches Fußsyndrom (DFS)",
    "Diabetischer Fuß": "Diabetisches Fußsyndrom (DFS)",
    "neuropathisches Ulkus": "Diabetisches Fußsyndrom (DFS)",
    "Diabetisches Fußulkus (mehrere flache Ulzera)": "Diabetisches Fußsyndrom (DFS)",
    "Plantare Fußulzera, wahrscheinliches diabetisches/neuropathisches Fußulkus": "Diabetisches Fußsyndrom (DFS)",
    "Plantare Fußulzeration (vermutet neuropathisch/diabetisches Fußulkus)": "Diabetisches Fußsyndrom (DFS)",
    "Fußulkus (V. a. neuropathisch/diabetisch), druckbedingt": "Diabetisches Fußsyndrom (DFS)",
    "Plantare Ulzeration (druckbedingt/neuropathisch, vereinbar mit diabetischem Fußulkus)": "Diabetisches Fußsyndrom (DFS)",
    "Plantarer Druckulkus des Vorfußes (vereinbar mit diabetischem Fußulkus), multiple Ulcera": "Diabetisches Fußsyndrom (DFS)",
    "Diabetisches Fußulkus, hochgradig destruierende Fußwunde (diabetisch-ischämisches Fußulcus, feuchte Gangrän…)": "Diabetisches Fußsyndrom (DFS)",
    "mit deutlichen Zeichen einer lokalen Infektion und chronisch entzündlicher Hautveränderungen": "Diabetisches Fußsyndrom (DFS)",
    "hochgradig destruierende Fußwunde": "Diabetisches Fußsyndrom (DFS)",

    # -------------------------------------------------------------
    # 7. ULCUS CRURIS ARTERIOSUM / ISCHÄMISCHES ULKUS
    # -------------------------------------------------------------
    "Ulcus cruris arteriosum": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "Ulkus cruris arteriosum": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "ischämisches Ulkus": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "ischämisches Ulcus": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "arterielles Ulkus": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "arterielles Ulcus": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "schwere Nekrose am Fuß rechts lateral und plantar, offene Geschwüre über den Malleolen lateral\ndeutet auf arterielles Ulcus hin": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "nekrotische Ischämische Fußwunde / Gangrän": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "nekrotische ischämische Fußwunde / Gangrän": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "Ischämische Nekrose/Gangrän des Fußes": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "Ischämische Nekrose / drohende Gangrän am Fuß": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "Ischämische Nekrose / Gangrän am Fuß": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "neuroischämisches bzw. arterielles Fußulkus": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "neuroischämisches bzw. arterielles Fußulcus": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "Ischämische, nekrotische Wunde (arterielles Ulcus möglich)": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "Nekrotische Fußwunde (z. B. Ulcus/Gangrän des Vorfußes)": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "Ischämischer Fußulkus / nekrotische Wunde (Gangränverdacht)": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "Gangränöse, nekrotische Fußwunde (Ulkus)": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "mumifizierte Zehen (D4 und D5), gleichzeitig Nekrose an der rechten Ferse": "Ulcus cruris arteriosum / Ischämisches Ulkus",
    "mumifizierte Zehen (D4/D5), Nekrose rechte Ferse": "Ulcus cruris arteriosum / Ischämisches Ulkus",

    # -------------------------------------------------------------
    # 8. ULCUS CRURIS VENOSUM
    # -------------------------------------------------------------
    "Ulcus cruris venosum": "Ulcus cruris venosum",
    "Ulkus cruris venosum": "Ulcus cruris venosum",
    "Ulcus cruris /  Gravitationsulcus: Ulcus cruris venosum": "Ulcus cruris venosum",
    "ausgeprägtes infiziertes Ulcus cruris, Ulcus cruris venosum": "Ulcus cruris venosum",
    "Adipositas-assoziiert": "Ulcus cruris venosum",
    "Ulcus cruris (vermutlich venös)": "Ulcus cruris venosum",
    "Ulcus cruris (vermutlich venös), chronische Wunde": "Ulcus cruris venosum",
    "Ulcus cruris (vermutlich venös), oberflächliche flächige Ulzeration": "Ulcus cruris venosum",
    "Ulcus cruris (vermutlich venös, Bildbeurteilung)": "Ulcus cruris venosum",
    "Ulcus cruris (wahrscheinlich venös)": "Ulcus cruris venosum",
    "Ulcus cruris (wahrscheinlich venös), klein/oberflächlich": "Ulcus cruris venosum",
    "Ulcus cruris venosum (Verdacht)": "Ulcus cruris venosum",
    "Ulcus cruris venosum (vermutet)": "Ulcus cruris venosum",
    "Ulcus cruris (V. a. venös)": "Ulcus cruris venosum",
    "Ulcus cruris (venös verdächtig) – großes, oberflächliches Ulkus": "Ulcus cruris venosum",
    "Ulcus cruris (venös vermutet)": "Ulcus cruris venosum",
    "Ulcus cruris venosum (venös-typisch)": "Ulcus cruris venosum",

    # -------------------------------------------------------------
    # 9. ULCUS CRURIS MIXTUM
    # -------------------------------------------------------------
    "Ulcus cruris mixtum": "Ulcus cruris mixtum",

    # -------------------------------------------------------------
    # 10. VERBRENNUNGSWUNDE
    # -------------------------------------------------------------
    "Verbrennungswunde": "Verbrennungswunde",
    "Verbrennung": "Verbrennungswunde",
    "Verbrennungswunde 1. bis 2. Grades": "Verbrennungswunde",
    "Verbrennung 2. Grades am Bein": "Verbrennungswunde",
    "Verbrennung Grad 1 bis 2 am rechten Fuß": "Verbrennungswunde",
    "Verbrennung 2 und 3 Grades nach 9 er Regel etwa 9 % Körperoberfläche": "Verbrennungswunde",
    "Verbrennungswunde am Arm Grad 2": "Verbrennungswunde",
    "traumatologische Wunde ( thermische Schädigung / Verbrennung 3. und 4. Grades": "Verbrennungswunde",
    "Verbrennung 2. und teilweise 3. Grades Oberfläche ca 9 %": "Verbrennungswunde",
    "Oberflächliche thermische Verletzung/Verbrennung (grad 2a) der Hand": "Verbrennungswunde",
    "Thermische Verletzung (Verbrennung Grad 2b, Blasenbildung)": "Verbrennungswunde",
    "Thermische Verletzung (Verbrennung/Verbrühung 2. Grades, bullös)": "Verbrennungswunde",
    "Verbrennung (thermische Verletzung), flächig": "Verbrennungswunde",
    "Thermische Verletzung – Verbrennung 2. Grades mit Blasenbildung": "Verbrennungswunde",
    "Verbrennung/Verbrühung Grad 2 (oberflächlich-partiell), großflächig": "Verbrennungswunde",
    "Verbrennung (bullös, partielle Hautschädigung)": "Verbrennungswunde",
    "Verbrennung (thermische Verletzung), großflächige Weichteilläsion": "Verbrennungswunde",
    "Verbrennungswunde (blasig, oberflächlich partiell)": "Verbrennungswunde",

    # -------------------------------------------------------------
    # 11. TRAUMATISCHE WUNDE (STRIKT: Nur echte Unfälle/Traumata/Bisse/Stiche!)
    # -------------------------------------------------------------
    "Traumatische Wunde": "Traumatische Wunde",
    "durch Insektenstich": "Traumatische Wunde",
    "Ulcus nach Stich": "Traumatische Wunde",
    "Ulcus unbekannter Herkunft, könnte traumatologisch bedingte Wunde sein, durch die Wunde bei unsachgemäßer Versorgung entstehen ulcerationen ebenfalls, nicht immer Krankheitsbedingt": "Traumatische Wunde",
    "Großflächige traumatische/sekundär heilende Wunde": "Traumatische Wunde",
    "Traumatische oder postoperativ sekundär heilende Wunde": "Traumatische Wunde",
    "Großflächige, oberflächliche traumatische Wunde / möglich Spalthaut-Entnahmestelle": "Traumatische Wunde",
    "Traumatische Weichteilverletzung mit Blasenbildung/Hämatom am Fuß (geschlossene Hautschädigung)": "Traumatische Wunde"
}

UNMAPPED_EXPLICIT_STRINGS = {
    "Plantares Ulcus linker Fuß, Ursachen Klärung notwendig, bei Diabetiker Prüfung ob Neuropathisch oder Angiopathische Ursache"
}

def map_wundtyp_explicit(val_str):
    if not val_str or val_str in ["keine Angabe", "nan", "?", "???", "Sonstiges"]:
        return "Enthaltung / keine Angabe"
    
    clean_str = str(val_str).strip()
    
    if clean_str in UNMAPPED_EXPLICIT_STRINGS:
        return clean_str

    if clean_str in EXPLICIT_WUNDTYP_RULES:
        return EXPLICIT_WUNDTYP_RULES[clean_str]
        
    for k, v in EXPLICIT_WUNDTYP_RULES.items():
        if k.lower() == clean_str.lower():
            return v

    v = clean_str.lower()
    
    if "nehme hier keine beurteilung vor" in v:
        return "Enthaltung / keine Angabe"

    if "gleiche beurteilung" in v:
        return "Dekubitus"

    if "traumatische/thermische" in v or "thermische" in v:
        return "Verbrennungswunde"

    if "könnte diabetischer ulcus sein auf grund einer neuropathie" in v:
        return "Diabetisches Fußsyndrom (DFS)"

    if "vermutetem diabetes" in v:
        return "Ulkus (Ätiologie unspezifisch)"

    if (" oder " in v or "dd " in v or "dd:" in v or "kombination" in v or "ätiologie unklar" in v or "genese unklar" in v or "ursache unklar" in v or "ursache nicht" in v or "nicht sicher" in v or "bild legt" in v or "verdacht anhand bild" in v or "bildbeurteilung" in v or "mangelernährung" in v or "könnte" in v or "nicht ausgeschlossen" in v) and not ("postop" in v or "platzbauch" in v or "dehiszen" in v):
        return "Ulkus (Ätiologie unspezifisch)"

    if "platzbauch" in v or "dehiszen" in v or "postop" in v or "op-wunde" in v or "spalthaut" in v or "meshgraft" in v:
        return "Postoperative Wunde / Dehiszenz"

    if "diabet" in v or "dfs" in v or "neuropathisch" in v:
        return "Diabetisches Fußsyndrom (DFS)"

    if "dekubitus" in v or "dekubital" in v or "dekubtis" in v or "druckul" in v or "druckgeschwür" in v or "epuap" in v or "fersendekubitus" in v or "fersenulkus" in v:
        return "Dekubitus"

    if "verbrenn" in v or "verbrüh" in v or "thermi" in v:
        return "Verbrennungswunde"

    if "mixtum" in v or "mischul" in v:
        return "Ulcus cruris mixtum"

    if "venö" in v or "venosum" in v or "cvi" in v:
        return "Ulcus cruris venosum"

    if "arteriel" in v or "arteriosum" in v or "ischäm" in v or "gangrän" in v or "pavk" in v or "mumifizier" in v:
        return "Ulcus cruris arteriosum / Ischämisches Ulkus"

    if "trauma" in v or "stich" in v or "insek" in v or "biss" in v or "schnitt" in v:
        return "Traumatische Wunde"

    if "ulcus" in v or "ulkus" in v or "ulzerat" in v or "ulcera" in v or "ulzera" in v:
        return "Ulkus (Ätiologie unspezifisch)"

    return clean_str
