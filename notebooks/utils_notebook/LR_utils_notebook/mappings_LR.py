# =====================================================================
# SPELLING MAPPING
# =====================================================================
SPELLING_MAPPING = {
    # Hier können Wortkorrekturen eingetragen werden
}

# =====================================================================
# MEDICAL MAPPINGS
# =====================================================================

# WUNDTYP MAPPING
WUNDTYP_GT_MAPPING = {
    # z.B. "Postoperative Wunde abdominal": ["Postoperative Wunde"]
    "Ulcus": ["Ulkus"],
    "Dekubtis": ["Dekubitus"],
    "Decubitus": ["Dekubitus"],
    "Ulcera": ["Ulzera"],
    "Ulcerationen": ["Ulzera"],
    "Ulcus decubitus": ["Dekubitus"],
    "Ulcus Dekubitus": ["Dekubitus"],
    "Ulcus dekubitus": ["Dekubitus"],

    # ---- Ulkus ----
    "zirkuläres Ulcus Unterschenkel (vermutlich Mischulcus)": ["Ulkus"],
    "Ulcus am Fussrücken": ["Ulkus"],
    "semizirkuläres Ulcus re Fuß": ["Ulkus"],
    "Ulcus, bei vermutetem Diabetes": ["Ulkus"],
    "Ulcus mit Stauung": ["Ulkus"],
    "Teils nekrotisches Ulcus an der linken Ferse.\nplantares Ulcus belegt mit Infektionszeichen": ["Ulkus"],
    "laterales Ulcus linker Fuß": ["Ulkus"],
    "Taschenbildendes Ulcus am linken Fußrücken": ["Ulkus"],
    "Fersenulcus / eventuell Mischulcus": ["Ulkus"],
    "Oberflächliches Ulcus (diffuse Defekte)": ["Ulkus"],
    "fibrinbelegtes Ulcus": ["Ulkus"],
    "Fibrinbelegtes Ulcus": ["Ulkus"],
    "Ulcus nach Meshgraft (zumindest lässt die Struktur darauf schließen), eventuell ist die Struktur aber einer Unterdrucktherapie geschuldet": ["Ulkus"],
    "belegter Ulcus": ["Ulkus"],
    "Oberflächliches Ulcus": ["Ulkus"],
    "Fibringbelegtes Ulcus": ["Ulkus"],
    "oberflächliches Ulcus": ["Ulkus"],
    "vermutlich Mischulcus am rechten Bein, höhe der Knöchel.\nSemizirkulär": ["Mischulkus"],
    "Infiziertes Ulcus mit freiliegender Sehne": ["Ulkus"],
    "Ulcus mit scheinender Hypergranulation oberhalb der Achillessehne": ["Ulkus"],
    "tiefes Ulcus im Fersenbereich": ["Ulkus"],
    "Ulcus nach Stich": ["Ulkus"],
    "Plantares Ulcus linker Fuß, Ursachen Klärung notwendig, bei Diabetiker Prüfung ob Neuropathisch oder Angiopathische Ursache": ["Ulkus"],
    "könnte arterieller Ulcus oder diabetischer Ulcus ( Angiopathie) auf Grund der Mangeldurchblutung  sein.": ["Ulkus"],
    "Ulcus unklarer Genese, könnte Venös oder arteriell oder mixum sein.\nBeachte kleine Nekrose an der Ferse plantar": ["Ulkus"],
    "Ulcus auf Grund von Mangelernährung des Gewebes, Druckschäden in Kombination mit Gefäßschäden": ["Ulkus"],
    "Ulcus unklarer Genese, könnte diabet. Ulcus sein, möglich ebenso durch traumatologische Ursachen": ["Ulkus"],
    "Ulcus lokal abgegrenzt. belegt könnte ebenso nekrotisch sein": ["Ulkus"],
    "Ulcus Ursache nicht genau definierbar": ["Ulkus"],
    "Ulcus. Ursache klären sollte es ein diabet. Fuß sein dann Prüfung ob angiopathisch oder neuropathisch,\nDruckentlastung und Ursachenbeseitigung.": ["Ulkus"],
    "Ulcus, durch die Mangelernährung ( keine Durchblutung) im Wundgebiet  könnte es sich um einen Dekubitus oder ulcus cruris handeln.": ["Ulkus"],
    "Ulcus unklarer Genese": ["Ulkus"],
    "Ulcus am Unterschenkel medial": ["Ulkus"],
    "Ulcus unbekannter Herkunft, könnte traumatologisch bedingte Wunde sein, durch die Wunde bei unsachgemäßer Versorgung entstehen ulcerationen ebenfalls, nicht immer Krankheitsbedingt": ["Ulkus"],
    "Ulcus, Lokalisation am Bein nicht genau definierbar": ["Ulkus"],
    "Ulcus unklarer Genese am Bein genaue Lokalisation nicht beurteilbar": ["Ulkus"],
    "Ulcus an der Achillessehne": ["Ulkus"],

    # ---- Ulkus cruris ----
    "Ulcus cruris venosum": ["Ulkus cruris venosum"],
    "Ulcus cruris li lateraler Malleolus": ["Ulkus cruris"],
    "Ulcus cruris": ["Ulkus cruris"],
    "Ulcus cruris /  Gravitationsulcus: Ulcus cruris venosum": ["Ulkus cruris venosum"],
    "schwere Nekrose am Fuß rechts lateral und plantar, offene Geschwüre über den Malleolen lateral\ndeutet auf arterielles Ulcus hin": ["Ulkus cruris arteriosum"],
    "Ulcus cruris möglich arteriell oder mixtum": ["Ulkus cruris"],
    "Ulcus cruris  unklarer Ursache": ["Ulkus cruris"],
    "Ulcus / warsch. Ulcus cruris, Ursache nicht klar, muss bestimmt werden": ["Ulkus cruris"],


    # ---- Ulzera ----
    "diffuse fibrinbelegte und teils infizierte Ulzera am rechten Fuß": ["Ulzera"],
    "semizirkuläres Ulcus": ["Ulzera"],
    "Ulcera rechter Fuß. könnte ursächlich diabetischer Fuß sein ( Neuropathie, Angiopathie) oder arterielles ulcus schäden auf Grund fehlender Durchblutung": ["Ulzera"],
    "schwere Ulzerationen am Fuß- mehrere offene Stellen, freiliegende Sehen, teilweise nekrotisch, belegt": ["Ulzera"],
    "superinfizierte Ulcration am rechen Fuß offene Ulcera": ["Ulzera"],
    "Ulcerationen bedingt durch Vaskulitis- Form der rheumatischen Erkrankung ( Autoimmunerkrankung)": ["Ulzera"],
    "offene ulcera": ["Ulzera"],

    # ---- Dekubitus ----
    "nekrotischer Defekt / Dekubitus": ["Dekubitus"],
    "nekrotischer Dekubitus li Ferse": ["Dekubitus"],
    "Dekubitus, vermutlich am Außenknöchel": ["Dekubitus"],
    "Fersendekubitus": ["Dekubitus"],
    "Dekubitus an der Ferse": ["Dekubitus"],
    "Dekubitus mit Nekrose": ["Dekubitus"],
    "tiefer Dekubitus": ["Dekubitus"],
    "Dekubitus mit Taschenbildung": ["Dekubitus"],
    "Dekubtis im Sakralbereich, großflächig": ["Dekubitus"],
    "oberflächlicher Dekubitus ( 2 Stück)": ["Dekubitus"],

    "Ulcus decubitus": ["Dekubitus"],
    "massives Ulcus dekubitus": ["Dekubitus"],
    "Ulcus Dekubitus": ["Dekubitus"],
    "Ulkus an der Ferse, warsch. Dekubitus nach EPUAP  Stadium 3": ["Dekubitus"],
    "Ulcus Dekubitus nach Epuap Grad 2 bis 3": ["Dekubitus"],
    "Ulcus dekubitus Ferse,  Stadium 3 / 4": ["Dekubitus"],
    "Ulcus decubitus Nach Epuap Grad 2 bis 3": ["Dekubitus"],
    "Dekubitus sacralbereich": ["Dekubitus"],
    "Dekubitus epuap Stadium 3 / 4": ["Dekubitus"],
    "Ulcus Dekubitus Epuap Grad 3 / 4": ["Dekubitus"],
    "Ulcus dekubitus": ["Dekubitus"],
    "Dekubitus Grad 2 oder 3 nach EPUAP.\nNicht genau zu definieren, ob sich Unterminierungen vorhanden sind.": ["Dekubitus"],
    "Ulkus Dekubitus am Os sacrum  nach Epuap Grad 2 / 3": ["Dekubitus"],
    "Ulcus Dekubitus Bereich OS Sacrum": ["Dekubitus"],

    # ── Verbrennung ──
    "Verbrennungswunde 1. bis 2. Grades": ["Verbrennungswunde"],
    "Verbrennung 2. Grades am Bein": ["Verbrennungswunde"],
    "Verbrennung Grad 1 bis 2 am rechten Fuß": ["Verbrennungswunde"],
    "Verbrennung 2 und 3 Grades nach 9 er Regel etwa 9 % Körperoberfläche": ["Verbrennungswunde"],
    "Verbrennungswunde am Arm Grad 2": ["Verbrennungswunde"],
    "traumatologische Wunde ( thermische Schädigung / Verbrennung 3. und 4. Grades": ["Verbrennungwunde"],
    "Verbrennung 2. und teilweise 3. Grades Oberfläche ca 9 %": ["Verbrennungswunde"],

    # ── Nekrose ──
    "mumifizierte Zehen (D4 und D5), gleichzeitig Nekrose an der rechten Ferse": ["Nekrose"],
    "nekrotischen Wunden am Fuß": ["Nekrose"],
    "siehe oben": ["Nekrose"],

    # ---- Diabetisches Fußulkus ----
    "könnte diabetischer ulcus sein auf grund einer neuropathie": ["Diabetisches Fußulkus"],
    "könnte ein diabetischer Fuß sein, Ulcus  nicht möglich,\ntraumatologische Indikation ebenso nicht ausgeschlossen": ["Diabetisches Fußulkus"],
    "Ulcus auf Grund von Mangeldurchblutung. Könnte diabetischer Fuß sein / angiopathisch bedingt.": ["Diabetisches Fußulkus"],

    # ── Sonstige ──
    "Platzbauch nach möglichem chirurgischen Eingriff": ["Platzbauch"],
    "möglicherweise ein feuchtes Gangrän": ["Ischämisches Fußulkus (Gangrän)"],
    "Postoperative Wunde abdominal": ["Postoperative Wunde"],
    "infantiles Hämangiom,": ["Hämangiom"],

}

# WUNDGRUND MAPPING
WUNDGRUND_GT_MAPPING = {
    # z.B. "Granulation": ["Granulation"]
    "nekrotisch": ["Nekrose"],
    "Fibrinbelegt": ["Fibrinbelag"],
    "Sauber, bis auf die aufgetragene Salbe": ["Sauber"],
    "Fibrinbelegte Wunde": ["Fibrinbelag"],
    "nekrotisch belegt": ["Nekrose", "Fibrinbelag"],
    "Fibringbelegt mit durschscheinendem Granulationsgewebe": ["Fibrinbelag", "Granulation"],
    "Mischuntergrund. Fibrinbelag, nekrotisch, teils mit Granulationsinseln": ["Mischuntergrund", "Fibrinbelag", "Nekrose", "Granulation"],
    "teilweise fibrinbelegt mit einzelnen Granulationsinseln": ["Fibrinbelag", "Granulation"],
    "sauberer Wundgrund mit Inseln von Granulation": ["Sauber", "Granulation"],
    "Fibrinbelegt mit einzelnen Granulationsinseln": ["Fibrinbelag", "Granulation"],
    "Fibrinbelegtes tiefes Ulcus": ["Fibrinbelag", "Ulzeration"],
    "Fibrinbelegt bei Wundrandepithelisierung": ["Fibrinbelag", "Wundrandepithelisierung"],
    "belegt mit Hypergranulation": ["Hypergranulation"],
    "Fibrinbelegte Wundverhältnisse": ["Fibrinbelag"],
    "Fibrinbelegt, zerklüftet": ["Fibrinbelag","Zerklüftet"],
    "Sauberer Wundgrund mit kleinen Fibrininseln": ["Sauber", "Fibrinbelag"],
    
}

# WUNDUMGEBUNG MAPPING
WUNDUMGEBUNG_GT_MAPPING = {
    # z.B. "Erythem / Rötung": ["Erythem / Rötung"]
}

# WUNDRAND MAPPING
WUNDRAND_GT_MAPPING = {
    # z.B. "Gerötet / entzündlich": ["Gerötet / entzündlich"]
}

# PRODUKT MAPPING (Präferenz- und Alternativprodukte)
PRODUKT_GT_MAPPING = {
    # z.B. "Suprasorb CNP": ["Suprasorb CNP"]
}

# DEBRIDEMENT MAPPING
DEBRIDEMENT_GT_MAPPING = {
    # z.B. "Chirurgisches Debridement": ["Chirurgisches Debridement"]
}

# LOKALISATION KEYWORDS
LOKALISATION_KEYWORDS = {
    "Abdomen": ["abdomen", "bauch"],
    "Bein": ["bein", "fuß", "zehe", "knöchel", "unterschenkel", "oberschenkel", "ferse"],
    "Arm": ["arm", "hand", "finger", "ellenbogen", "oberarm", "unterarm"],
    "Gesäß": ["gesäß", "sakral", "kreuzbein", "steißbein"],
    "Rücken": ["rücken"],
    "Flanke": ["flanke"],
    "Kopf": ["kopf", "hals", "nacken"],
    "Brust": ["brust", "thorax"]
}
