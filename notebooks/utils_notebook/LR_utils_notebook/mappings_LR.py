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

    # LLM
    # ---- Dekubitus ----
    "Dekubitus (Druckulkus)": ["Dekubitus"],
    "Dekubitus": ["Dekubitus"],
    "Dekubitus (Fersenulkus)": ["Dekubitus"],
    "Dekubitalulkus (Druckulcus) Ferse": ["Dekubitus"],
    "Druckulzer (Ferse/Fußulkus)": ["Dekubitus"],
    "Dekubitus (druckbedingtes Ulkus) an der Ferse": ["Dekubitus"],
    "Dekubitus (Druckulkus) Ferse": ["Dekubitus"],
    "Dekubitalulkus (Ferse)": ["Dekubitus"],
    "Dekubitalulkus (Druckulkus)": ["Dekubitus"],
    "Dekubitus (Druckulkus) der Ferse": ["Dekubitus"],
    "Dekubitalulkus (Druckulcus) an der Ferse": ["Dekubitus"],
    "Dekubitalulkus (Druckulkus) an der Ferse": ["Dekubitus"],
    "Dekubitus (Druckulzera)": ["Dekubitus"],

    # ---- Ulkus cruris ----
    "Ulcus cruris (vermutlich venös)": ["Ulkus cruris venosum"],
    "Ulcus cruris (wahrscheinlich venös)": ["Ulkus cruris venosum"],
    "Ulcus cruris": ["Ulkus cruris"],
    "Ulcus cruris (vermutlich venös), oberflächliche flächige Ulzeration": ["Ulkus cruris venosum","Ulkus"],

    "Ulcus cruris venosum (Verdacht)": ["Ulkus cruris venosum"],
    "Ulcus cruris (vermutlich venös, Bildbeurteilung)": ["Ulkus cruris venosum"],
    "Ulcus cruris (chronisch, Ätiologie unklar)": ["Ulkus cruris"],
    "Ulcus cruris (vermutet, chronische Unterschenkelwunde)": ["Ulkus cruris"],
    "Ulcus cruris (vermutet venös)": ["Ulkus cruris venosum"],
    "Ulcus cruris venosum (vermutet)": ["Ulkus cruris venosum"],
    "Ulcus cruris (wahrscheinlich venös), klein/oberflächlich": ["Ulkus cruris venosum"],
    "Ulcus cruris (Verdacht anhand Bild)": ["Ulkus cruris"],
    "Ulcus cruris (unklare Ätiologie)": ["Ulkus cruris"],
    "Ulcus cruris (vermutlich venös), chronische Wunde": ["Ulkus cruris venosum"],

    # ---- Ulkus ----
    "Traumatische/chronische Wunde (Fußulkus unklarer Genese)": ["Ulkus"],
    "Chronisches Fußulkus (mehrere Ulzerationen)": ["Ulkus"],
    "Traumatische/infizierte Ulzeration (kleines Ulkus)": ["Ulkus"],
    "Ulzeration, unklare Genese (oberflächlich, mit Nekrose/Fibrin)": ["Ulkus"],
    "Nekrotische Ulzeration (unklare Genese, möglich druck-/ischämiebedingt)": ["Ulkus"],

    # ---- Ulzera ----
    "Mehrere Ulzera am Fuß; Ätiologie im Bild nicht sicher (druck-/ischämisch möglich)": ["Ulzera"],
    "Mehrere nekrotisch-belegte Ulzera am Fuß (druck-/ischämieassoziiert möglich)": ["Ulzera"],
    "Multiple chronische Ulzera am Fuß (nur Bildbeurteilung)": ["Ulzera"],

    # ---- Diabetisches Fußulkus ----
    "Diabetisches Fußulkus (mehrere flache Ulzera)": ["Diabetisches Fußulkus"],
    "Plantare Fußulzeration (vermutet neuropathisch/diabetisches Fußulkus)": ["Diabetisches Fußulkus"],
    "Plantare Fußulzera, wahrscheinliches diabetisches/neuropathisches Fußulkus": ["Diabetisches Fußulkus"],

    # ---- Ischämisch / Nekrose ----
    "Ischämische, nekrotische Wunde (arterielles Ulcus möglich)": ["Ischämisches Fußulkus (Gangrän)"],
    "Nekrotische Fußwunde (z. B. Ulcus/Gangrän des Vorfußes)": ["Ischämisches Fußulkus (Gangrän)"],

    # ---- Verbrennung ----
    "Oberflächliche thermische Verletzung/Verbrennung (grad 2a) der Hand": ["Verbrennungswunde"],
    "Verbrennung (thermische Verletzung), flächig": ["Verbrennungswunde"],
    "Thermische Verletzung (Verbrennung/Verbrühung 2. Grades, bullös)": ["Verbrennungswunde"],
    "Thermische Verletzung (Verbrennung Grad 2b, Blasenbildung)": ["Verbrennungswunde"],

    # ---- Postoperative Wunde ----
    "Postoperative Wunde (dehiszient, sekundär heilend)": ["Postoperative Wunde"],
    "Postoperative Wunde (Spalthautentnahmestelle)": ["Postoperative Wunde"],
    "Postoperative/traumatische sekundär heilende Wunde": ["Postoperative Wunde","Traumatische Wunde"],
    "Traumatische oder postoperativ sekundär heilende Wunde": ["Postoperative Wunde","Traumatische Wunde"],

    # ---- Sonstige ----
    "Großflächige traumatische/sekundär heilende Wunde": ["Traumatische Wunde"],
    "Kleiner Abszess/Sinusöffnung (infizierte oberflächliche Hautläsion)": ["Abszess"],

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

    "belegt, teilweise nekrotisch": ["Belag", "Nekrose"],
    "stark infiziert, massiv belegt": ["Infektion", "Belag"],
    "verbrannte  Epidermis": ["Verbrennung"],
    "belegt, nekrotisch": ["Belag", "Nekrose"],
    "massive großflächige Verbrennung teilweise 4. Grades, je mehr es vom Wundzentrum nach außen geht werden Verbrennungen 3 7 2. und 1. Grades sichtbar. Nach der 9 er regel könnten hier bis zu 9 % der Körperoberfläche geschädigt sein": ["Verbrennung"],
    "Verbrennungen, Blasenbildung, offene Wunden keine verbrannten Sehnen / Knochen  epidermis geschädigt": ["Verbrennung", "Blasenbildung"],
    "stark belgtes Ulcus, teilweise einzelne Granulationsinseln,": ["Belag", "Granulation"],
    "hämatös": ["Hämatom"],
    "Fußwunde: Nekrotisch  Unterschenkelwunde fibrinös belegt,": ["Nekrose", "Fibrinbelag"],
    "sehr ausgeprägte massive Nekrose, teilweise frei liegende Strukturen, blutig seröses Exsudat": ["Nekrose", "Freiliegende Strukturen", "Exsudat"],
    "belegte Wunde, teilweise infiziert": ["Belag", "Infektion"],
    "Nekrotische und fibrinös belegte Wunde- auf Grund der Mazeration nach plantar hin könnte mäßige Exsudation auftreten. Wundinfektion möglich": ["Nekrose", "Fibrinbelag", "Mazeration"],
    "fibrinös belegt, zum Teil mit Granulationsinseln, teilweise freiliegende Sehnen.\nNekrose plantar wandständig trocken": ["Fibrinbelag", "Granulation", "Freiliegende Sehnen", "Nekrose"],
    "mehrere Stadien zu erkennen, nekrotisch, belegt, teilweise granuliert": ["Nekrose", "Belag", "Granulation"],
    "Nekrotisch und durch Infektion belegt, Wunde bildet Geruch, Frage der Keimbestimmung wichtig, Wundabstrich notwendig,": ["Nekrose", "Infektion"],
    "teilweise nekrotisch, belegt": ["Nekrose", "Belag"],
    "offenen stelle entzündet. belegt, nekrotisch, geschlossene stelle nekrotisch": ["Entzündung", "Belag", "Nekrose"],
    "wandständige Nekrose, Prüfung, ob Knochen / Sehnen betroffen sind. Unbedingt chirurgisch intervenieren.\nDruckentlastung essentiell.": ["Nekrose"],
    "fibrinös belegt, unterminierte Wundränder siehe punktierte Markierung\nEventuelle freie Sehnen": ["Fibrinbelag", "Unterminierung","Freiliegende Sehnen"],
    "freiliegende Sehnen Strang 5, freiliegende Knochen,\nteilweise nekrotisch": ["Freiliegende Sehnen", "Freiliegende Knochen", "Nekrose"],
    "großes Ulcus: belegt, teilweise nekrotisch\nZehe: trockene Nekrose- bitte nicht durch autolytisches Débridement anfeuchten. Zeh fällt irgendwann ab, da die Durchblutung massiv gestört ist. Gefäßstatus prüfen und gfls. sanieren": ["Belag", "Nekrose"],
    "Kleine Nekrose oberhalb des großen offenen Ulcus, muss mit versorgt werden\nsonstig massiv belegt, Nekrosenbildung bei Nichtbehandlung wahrscheinlich. Prüfung ob knöcherne Strukturen / Sehnen betroffen sind": ["Nekrose", "Belag"],
    "belegt, teilweise nekrotisch, teilweise überschießende Granulation": ["Belag", "Nekrose", "Hypergranulation"],
    "stark belegt, neben Fibrin könnte es sich auch um feuchte, wandständige Nekrosen handeln": ["Fibrinbelag"],
    "Granulation und Beläge gleichzeitig": ["Granulation", "Belag"],
    "belegt, mäßige Exsudation Infektion möglich": ["Belag", "Exsudat"],
    "leichte Granulation, belegt mit Fibrin, 2 Inseln Beurteilung hier schwer, da nicht genau zu erkennen sind, ob es ich um Nekrosen handelt.": ["Granulation", "Fibrinbelag"],
    "belegt, hypergranulation": ["Belag", "Hypergranulation"],
    "nekrotisch und fibrinös belegt": ["Nekrose", "Fibrinbelag"],
    "belegt, teilweise kleine Nekrosen, könnte infiziert sein": ["Belag", "Nekrose"],
    "kleinere Nekrosen, belegt": ["Nekrose", "Belag"],
    "belegt, teilweise nekrotisch könnte infiziert sein": ["Belag", "Nekrose"],
    "grünlich belegt, deutet auf Infektion hin, Nekrosen am  Wundgrund belegt": ["Belag", "Infektion", "Nekrose"],
    "stark belegte, super infizierte Wunde, teilweise freiliegende Strukturen,\nNekrosen.": ["Belag", "Infektion", "Freiliegende Strukturen", "Nekrose"],
    "stark geschädigt, nekrotisch, fibrinös belegt, freiliegende Sehnen / Knochen": ["Nekrose", "Fibrinbelag", "Freiliegende Sehnen", "Freiliegende Knochen"],
    "Granulationsgewebe, teilweise fibrinös belegt, Biofilm": ["Granulation", "Fibrinbelag", "Biofilm"],
    "belegt, fibrinös, nekrotisch": ["Fibrinbelag", "Nekrose"],
    "Granulationsinseln, fibrinös belegt": ["Granulation", "Fibrinbelag"],
    "belegt, teilweise kleine Nekrosen, könnte infiziert sein, belegt": ["Belag", "Nekrose"],
    "belegt, teilweise kleine Nekrosen freiliegende Sehne sichtbar": ["Belag", "Nekrose", "Freiliegende Sehnen"],
    "tiefer Dekubitus Wundgrund belegt, Taschenbildung teilweise nekrotisch": ["Belag", "Taschenbildung", "Nekrose"],
    "feuchte Nekrose,": ["Nekrose"],
    "nekrotisch, wandständige Nekrosen": ["Nekrose"],
    "nekrotisch, feuchte nekrose": ["Nekrose"],
    "fleischige Wunde mit Taschenbildung nach Feststellung der Ausdehnung": ["Granulation", "Taschenbildung"],
    "gerötet, stark geschädigt, teilweise nekrotisch belegt": ["Rötung", "Nekrose", "Belag"],
    
}

# EXSUDAT MAPPING
EXSUDAT_GT_MAPPING = {
    # z.B. "Annahme stark": ["Stark"]
    # ── Allgemeine Grundregeln ──
    "kein": ["Keine"],
    "keine": ["Keine"],
    "trocken": ["Keine"],
    "schwach": ["Leicht"],
    "gering": ["Leicht"],
    "wenig": ["Leicht"],
    "leicht": ["Leicht"],
    "mäßig": ["Mäßig"],
    "mässig": ["Mäßig"],
    "mäfig": ["Mäßig"],
    "mittel": ["Mäßig"],
    "mittelmäßig": ["Mäßig"],
    "mittelmässig": ["Mäßig"],
    "stark": ["Stark"],
    "hoch": ["Stark"],
    "Annahme stark": ["Stark"],

    # ── Einzelwerte ──
    "vermutlich mässig": ["Mäßig"],
    "vermutlich mittelmässig": ["Mäßig"],
    "vermutlich mittelmäßig": ["Mäßig"],
    "vermutlich mäßig": ["Mäßig"],
    "vermutlich mittel": ["Mäßig"],
    "Mässig": ["Mäßig"],
    "scheint mäßig zu sein": ["Mäßig"],
    "wahrscheinlich mittelmäßig vorhanden": ["Mäßig"],
    "nicht genau definierbar, aus der Erfahrung heraus mäßige Exsudation": ["Mäßig"],
    "blutig bis serös teilweise vorhanden dann eher mäßig": ["Mäßig"],
    "vermutlich gering": ["Leicht"],
    "keine Angabe möglich / eher wenig": ["Leicht"],
    "keine Angabe möglich, vermutlich gering": ["Leicht"],
    "vermutlich wenig": ["Leicht"],
    "vermutlich kaum": ["Leicht"],
    "keine Angabe möglich / vermutlich wenig": ["Leicht"],
    "eher weniger": ["Leicht"],
    "eher wenig": ["Leicht"],
    "sehr gering": ["Leicht"],
    "könnte eher schwach sein": ["Leicht"],
    "vermutlich hoch": ["Stark"],
    "nicht beurteilbar, vermutlich stark": ["Stark"],
    "vermutlich hohe Exsudation": ["Stark"],
    "vermutlich starke Exsudation": ["Stark"],
    "mittelstark": ["Stark"],
    "keine Angabe möglich, vermutlich trocken": ["Keine"],
    "keine Angabe möglich / vermutlich mässig": ["Mäßig"],

    # ── Komplexe / Mehrteilige Angaben ──
    "geschlossene stelle kein bis wenig exsudat, offenen stelle mäßig": ["Leicht", "Mäßig"],
    "nekrosen: kein exsudat. unterschenkel mäßig": ["Leicht", "Mäßig"],
    "große wunde: stark, da mazerationen am wundrand kleine nekrose: trocken": ["Mäßig", "Stark"],

    # ── Bereiche ──
    "schwach bis mäßig": ["Leicht", "Mäßig"],
    "schwach bin mäßig": ["Leicht", "Mäßig"],
    "leicht bis mäßig": ["Leicht", "Mäßig"],
    "leichte bis mäßige exsudation": ["Leicht", "Mäßig"],
    "eher schwach b is mäßig": ["Leicht", "Mäßig"],
    "leicht bis mittel": ["Leicht", "Mäßig"],
    "mäßig bis stark": ["Mäßig", "Stark"],
    "mittel bis stark": ["Mäßig", "Stark"],
    "mäßig bis stark, sicher ist eine Geruchsbildung süßlich aromatisch teilweise beschrieben als traubenartig": ["Mäßig", "Stark"],
    "warsch hoch bis sehr hoch,  klare exsudation": ["Stark", "Sehr Stark"],
    "schwach bis nicht vorhanden": ["Keine", "Leicht"],
    "gering bis gar nicht": ["Keine", "Leicht"],
    "keine genaue Angabe möglich, sieht eher trocken bis leicht exsudierend aus": ["Keine", "Leicht"],
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
    # ---- Suprasorb A + Ag ----
    "Suprasorb A + Ag": ["Suprasorb A + Ag"],
    "Suprasorb A + Ag (Kompresse)": ["Suprasorb A + Ag"],
    "Suprasorb A + Ag Kompresse": ["Suprasorb A + Ag"],
    "Suprasorb A + Ag Tamponade": ["Suprasorb A + Ag"],

    # ---- Suprasorb A Pro ----
    "Suprasorb A Pro": ["Suprasorb A Pro"],
    "Suprasorb A Pro (Kompresse)": ["Suprasorb A Pro"],
    "Suprasorb A Pro (Tamponade)": ["Suprasorb A Pro"],
    "Suprasorb A Pro Kompresse": ["Suprasorb A Pro"],
    "Suprasorb A Pro Tamponade": ["Suprasorb A Pro"],

    # ---- Suprasorb Liquacel Pro ----
    "Suprasorb Liquacel Pro": ["Suprasorb Liquacel Pro"],
    "Suprasorb Liquacel Pro (Kompresse)": ["Suprasorb Liquacel Pro"],
    "Suprasorb Liquacel Pro (Tamponade)": ["Suprasorb Liquacel Pro"],
    "Suprasorb Liquacel Pro Kompresse": ["Suprasorb Liquacel Pro"],
    "Suprasorb Liquacel Pro Tamponade": ["Suprasorb Liquacel Pro"],

    # ---- Suprasorb P ----
    "Suprasorb P": ["Suprasorb P"],
    "Suprasorb P (nicht klebend)": ["Suprasorb P"],
    "Suprasorb P (selbstklebend)": ["Suprasorb P"],
    "Suprasorb P (self-adhesive, sacrum)": ["Suprasorb P"],
    "Suprasorb P nicht klebend": ["Suprasorb P"],
    "Suprasorb P heel (selbstklebend)": ["Suprasorb P"],

    # ---- Suprasorb P + PHMB ----
    "Suprasorb P + PHMB": ["Suprasorb P + PHMB"],

    # ---- Suprasorb P Sensiflex ----
    "Suprasorb P SensiFlex (border rechteckig)": ["Suprasorb P Sensiflex"],
    "Suprasorb P SensiFlex border": ["Suprasorb P Sensiflex"],
    "Suprasorb P SensiFlex border rechteckig": ["Suprasorb P Sensiflex"],
    "Suprasorb P SensiFlex multisite border": ["Suprasorb P Sensiflex"],
    "Suprasorb P Sensiflex": ["Suprasorb P Sensiflex"],

    # ---- Suprasorb P Sensitive ----
    "Suprasorb P Sensitive": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive (heel)": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive (nicht klebend)": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive (selbstklebend)": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive (selbstklebend) als abdeckender Verband": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive heel": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive heel (selbstklebend) – als polsternde, absorbierende Sekundärlage über der Tamponade": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive sacrum": ["Suprasorb P Sensitive"],
    "Suprasorb P sensitive selbstklebend": ["Suprasorb P Sensitive"],

    # ---- Suprasorb X ----
    "Suprasorb X": ["Suprasorb X"],
    "Suprasorb X Kompresse": ["Suprasorb X"],

    # ---- Suprasorb X Pro ----
    "Suprasorb X Pro": ["Suprasorb X Pro"],
    "Suprasorb X Pro (Kompresse)": ["Suprasorb X Pro"],
    "Suprasorb X Pro Kompresse": ["Suprasorb X Pro"],

    # ---- Suprasorb X + PHMB ----
    "Suprasorb X + PHMB": ["Suprasorb X + PHMB"],
    "Suprasorb X + PHMB (Kompresse)": ["Suprasorb X + PHMB"],
    "Suprasorb X + PHMB Kompresse": ["Suprasorb X + PHMB"],

    # ---- Suprasorb G ----
    "Suprasorb G Gel-Kompresse": ["Suprasorb G Gel-Kompresse"],

    # ---- Suprasorb H ----
    "Suprasorb H": ["Suprasorb H"],

    # ---- Suprasorb F / F Protect ----
    "Suprasorb F": ["Suprasorb F"],
    "Suprasorb F Protect": ["Suprasorb F Protect"],

    # ---- Lomatuell Pro / H ----
    "Lomatuell Pro": ["Lomatuell Pro"],
    "Lomatuell H": ["Lomatuell H"],

    # ---- Vliwasorb Pro / sensitive ----
    "Vliwasorb Pro": ["Vliwasorb Pro"],
    "Vliwasorb sensitive": ["Vliwasorb sensitive"],

    # ---- Vliwazell / Vliwazell Pro ----
    "Vliwazell": ["Vliwazell"],
    "Vliwazell Pro": ["Vliwazell Pro"],
    "Vliwazell Pro als abdeckender Verband": ["Vliwazell Pro"],
    "Vliwazell Pro – als hochabsorbierende Sekundärlage über der Tamponade": ["Vliwazell Pro"],

    # ---- Vliwaktiv Ag ----
    "Vliwaktiv Ag": ["Vliwaktiv Ag"],
    "Vliwaktiv Ag Saugkompresse": ["Vliwaktiv Ag"],
    "Vliwaktiv Ag Tamponade": ["Vliwaktiv Ag"],

    # ---- Solvaline N ----
    "Solvaline N": ["Solvaline N"],

    # ---- Metalline ----
    "Metalline Kompresse": ["Metalline Kompresse"],

    # ---- Curafix / Porofix / Silkafix ----
    "Curafix H": ["Curafix H"],
    "Porofix": ["Porofix"],
    "Silkafix": ["Silkafix"],

    # ---- Mollelast ----
    "Mollelast": ["Mollelast"],
    "Mollelast (Elastische Fixierbinde)": ["Mollelast"],
    "Mollelast haft latexfrei": ["Mollelast haft latexfrei"],

    # ---- Haftelast ----
    "Haftelast latexfrei": ["Haftelast latexfrei"],
    "Haftelast latexfrei (kohäsive Fixierbinde)": ["Haftelast latexfrei"],

    # ---- ActiFast / tg ----
    "ActiFast": ["ActiFast"],
    "ActiFast Schlauchverband": ["ActiFast"],
    "tg Schlauchverband": ["tg Schlauchverband"],

    # ---- Curapor ----
    "Curapor": ["Curapor"],
    "Curapor transparent": ["Curapor transparent"],

    # ---- Sonstige GT-Produkte ----
    "Suprasorb CNP": ["Suprasorb CNP"],
    "amorphes Gel": ["amorphes Gel"],
    "Fixierbinde": ["Fixierbinde"],
    "Fixierbinden": ["Fixierbinde"],
    "Universalbinde": ["Universalbinde"],
    "Universalbinden": ["Universalbinde"]
}

# DEBRIDEMENT MAPPING
DEBRIDEMENT_GT_MAPPING = {
    # z.B. "Chirurgisches Debridement": ["Chirurgisches Debridement"]
}

# LOKALISATION KEYWORDS
LOKALISATION_KEYWORDS = {
    "Abdomen": ["abdomen", "bauch"],
    "Fuß": ["fuß", "fuss", "zehe", "ferse", "fußsohle", "fußrücken", "plantar", "vorfuß", "malleol", "achillessehne"],
    "Bein": ["bein", "knöchel", "unterschenkel", "oberschenkel", "knie"],
    "Hand": ["hand", "finger", "handgelenk"],
    "Arm": ["arm", "ellenbogen", "oberarm", "unterarm", "bizeps"],
    "Gesäß": ["gesäß", "sakral", "kreuzbein", "steißbein", "os sacrum", "sacral",
              "rima ani", "steiß", "trochanter"],
    "Rücken": ["rücken"],
    "Flanke": ["flanke"],
    "Kopf": ["kopf", "hals", "nacken"],
    "Brust": ["brust", "thorax"]
}
