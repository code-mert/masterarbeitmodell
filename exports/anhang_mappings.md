# Anhang: Medizinisches Mappings-Register (Normalisierungsschema)

Dieses Dokument enthält alle verwendeten Mapping-Tabellen zur Normalisierung von Freitext-Angaben, Experten-Ground-Truths und Modell-Vorhersagen aus `mappings.py` und `mappings_LR.py`.

## 1. Allgemeines / NursIT Normalisierungsschema (`mappings.py`)

### 1.WUNDTYP_GT_MAPPING

**Anzahl Einträge:** 143

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `["ausgedehnte, tiefe, nekrotische Ulzeration"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["ausgedehntes, tiefes chronisches Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["ausgeprägtes infiziertes Ulcus cruris","Ulcus cruris venosum"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["chronische Fußwunde / Ulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["chronisches Ulkus cruris"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["chronisches Ulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Dekubitus","Diabetisches Fußulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Dekubitus","Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Dekubitus"]` | `Dekubitus` |
| `["Diabetisches Fußulkus","hochgradig destruierende Fußwunde"]` | `Diabetisches Fußsyndrom (DFS)` |
| `["Diabetisches Fußulkus","ischämisches Ulkus"]` | `Diabetisches Fußsyndrom (DFS)` |
| `["Diabetisches Fußulkus","mit deutlichen Zeichen einer lokalen Infektion und chronisch entzündlicher Hautveränderungen"]` | `Diabetisches Fußsyndrom (DFS)` |
| `["Diabetisches Fußulkus"]` | `Diabetisches Fußsyndrom (DFS)` |
| `["Extravasationsverletzung"]` | `Extravasationsverletzung` |
| `["Gravitationsulzera/Druckulzera"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["großflächiges, flaches chronisches Ulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["kleines, oberflächliches Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["multiple infizierte chronische Fußulzera"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["multiple kleine Ulzera"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["nekrotische Fersenwunde","Dekubitus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["nekrotische ischämische Fußwunde / Gangrän"]` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `["neuroischämisches bzw. arterielles Fußulkus"]` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `["Postoperative Wunde"]` | `Postoperative Wunde / Dehiszenz` |
| `["rundlich-ovales Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["tiefer reichende Ulzerationen am Unterschenkel mit chronisch entzündlicher Umgebung"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Traumatische Wunde","durch Insektenstich"]` | `Traumatische Wunde` |
| `["Ulcus cruris venosum","Adipositas-assoziiert"]` | `Ulcus cruris venosum` |
| `["Ulcus cruris venosum","venös-lymphatischem Ulcus"]` | `Ulcus cruris venosum` |
| `["Ulcus cruris venosum"]` | `Ulcus cruris venosum` |
| `["Ulcus Fußrücken mit deutlicher Gewebedestruktion und freiliegender Sehnenstruktur"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Ulkus cruris"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Ulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["ulzeriertes infantiles Hämangiom mit zentraler Nekrose"]` | `ulzeriertes infantiles Hämangiom mit zentraler Nekrose` |
| `["vaskulitischen Ulzera","möglicher kutaner Vaskulitis"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Verbrennungswunde"]` | `Verbrennungswunde` |
| `arterielles Ulcus` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `Ausgedehnte feuchte Nekrose` | `Ausgedehnte feuchte Nekrose` |
| `Ausgetrtenes Blut oder Lymphe aus den entsprechenden Gefäßen mit Verteilung an der betroffenen Extremität` | `Ulkus (Ätiologie unspezifisch)` |
| `belegter Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Dekubitus` | `Dekubitus` |
| `Dekubitus an der Ferse` | `Dekubitus` |
| `Dekubitus epuap Stadium 3 / 4` | `Dekubitus` |
| `Dekubitus Grad 2 oder 3 nach EPUAP.
Nicht genau zu definieren, ob sich Unterminierungen vorhanden sind.` | `Dekubitus` |
| `Dekubitus mit Nekrose` | `Dekubitus` |
| `Dekubitus mit Taschenbildung` | `Dekubitus` |
| `Dekubitus sacralbereich` | `Dekubitus` |
| `Dekubitus, vermutlich am Außenknöchel` | `Dekubitus` |
| `Dekubtis im Sakralbereich, großflächig` | `Dekubitus` |
| `diffuse fibrinbelegte und teils infizierte Ulzera am rechten Fuß` | `Ulkus (Ätiologie unspezifisch)` |
| `Fersendekubitus` | `Dekubitus` |
| `Fersenulcus / eventuell Mischulcus` | `Ulcus cruris mixtum` |
| `Fibrinbelegtes Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `fibrinbelegtes Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Fibringbelegtes Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `gleiche Beurteilung wie Wunde 53` | `Dekubitus` |
| `Hypergranulation nach Verbrennung` | `Verbrennungswunde` |
| `Hämangiom ist ein Spezialgebiet. In der Regel ist dieses innerhalb des ersten Lebensjahres rückläufig.
Deshalb nehme ich hier keine Beurteilung vor.` | `Hämangiom ist ein Spezialgebiet. In der Regel ist dieses innerhalb des ersten Lebensjahres rückläufig.
Deshalb nehme ich hier keine Beurteilung vor.` |
| `infantiles Hämangiom,` | `infantiles Hämangiom,` |
| `Infizierte Wunden am linken Oberarm / Innenseitig` | `Infizierte Wunden am linken Oberarm / Innenseitig` |
| `Infiziertes Ulcus mit freiliegender Sehne` | `Ulkus (Ätiologie unspezifisch)` |
| `könnte arterieller Ulcus oder diabetischer Ulcus ( Angiopathie) auf Grund der Mangeldurchblutung  sein.` | `Ulkus (Ätiologie unspezifisch)` |
| `könnte diabetischer ulcus sein auf grund einer neuropathie` | `Ulkus (Ätiologie unspezifisch)` |
| `könnte ein diabetischer Fuß sein, Ulcus  nicht möglich,
traumatologische Indikation ebenso nicht ausgeschlossen` | `Ulkus (Ätiologie unspezifisch)` |
| `laterales Ulcus linker Fuß` | `Ulkus (Ätiologie unspezifisch)` |
| `massives Ulcus dekubitus` | `Dekubitus` |
| `mumifizierte Zehen (D4 und D5), gleichzeitig Nekrose an der rechten Ferse` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `möglicherweise ein feuchtes Gangrän` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `nekrotischen Wunden am Fuß` | `nekrotischen Wunden am Fuß` |
| `nekrotischer Defekt / Dekubitus` | `Dekubitus` |
| `nekrotischer Dekubitus li Ferse` | `Dekubitus` |
| `oberflächlicher Dekubitus ( 2 Stück)` | `Dekubitus` |
| `Oberflächliches Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `oberflächliches Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Oberflächliches Ulcus (diffuse Defekte)` | `Ulkus (Ätiologie unspezifisch)` |
| `offene ulcera` | `Ulkus (Ätiologie unspezifisch)` |
| `plantares ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Plantares Ulcus linker Fuß, Ursachen Klärung notwendig, bei Diabetiker Prüfung ob Neuropathisch oder Angiopathische Ursache` | `Plantares Ulcus linker Fuß, Ursachen Klärung notwendig, bei Diabetiker Prüfung ob Neuropathisch oder Angiopathische Ursache` |
| `Platzbauch nach möglichem chirurgischen Eingriff` | `Postoperative Wunde / Dehiszenz` |
| `Postoperative Wunde abdominal` | `Postoperative Wunde / Dehiszenz` |
| `pseudomas besiedeltes teils nekrotisches Ulcus.
Semizirkulär` | `Ulkus (Ätiologie unspezifisch)` |
| `rechter Fuß lateral/ malleolär` | `rechter Fuß lateral/ malleolär` |
| `schwere Nekrose am Fuß rechts lateral und plantar, offene Geschwüre über den Malleolen lateral
deutet auf arterielles Ulcus hin` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `schwere Ulzerationen am Fuß- mehrere offene Stellen, freiliegende Sehen, teilweise nekrotisch, belegt` | `Ulkus (Ätiologie unspezifisch)` |
| `semizirkuläres Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `semizirkuläres Ulcus re Fuß` | `Ulkus (Ätiologie unspezifisch)` |
| `superinfizierte Ulcration am rechen Fuß offene Ulcera` | `Ulkus (Ätiologie unspezifisch)` |
| `Taschenbildendes Ulcus am linken Fußrücken` | `Ulkus (Ätiologie unspezifisch)` |
| `Teils nekrotisches Ulcus an der linken Ferse.
plantares Ulcus belegt mit Infektionszeichen` | `Ulkus (Ätiologie unspezifisch)` |
| `tiefer Dekubitus` | `Dekubitus` |
| `tiefes Ulcus im Fersenbereich` | `Ulkus (Ätiologie unspezifisch)` |
| `traumatologische Wunde ( thermische Schädigung / Verbrennung 3. und 4. Grades` | `Verbrennungswunde` |
| `Ulcera rechter Fuß. könnte ursächlich diabetischer Fuß sein ( Neuropathie, Angiopathie) oder arterielles ulcus schäden auf Grund fehlender Durchblutung` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcerationen bedingt durch Vaskulitis- Form der rheumatischen Erkrankung ( Autoimmunerkrankung)` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus / warsch. Ulcus cruris, Ursache nicht klar, muss bestimmt werden` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus am Fussrücken` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus am Unterschenkel medial` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus an der Achillessehne` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus auf Grund von Mangeldurchblutung. Könnte diabetischer Fuß sein / angiopathisch bedingt.` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus auf Grund von Mangelernährung des Gewebes, Druckschäden in Kombination mit Gefäßschäden` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris` | `Ulkus (Ätiologie unspezifisch)` |
| `ulcus cruris` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris  unklarer Ursache` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris /  Gravitationsulcus: Ulcus cruris venosum` | `Ulcus cruris venosum` |
| `Ulcus cruris li lateraler Malleolus` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris möglich arteriell oder mixtum` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris venosum` | `Ulcus cruris venosum` |
| `Ulcus decubitus` | `Dekubitus` |
| `Ulcus decubitus Nach Epuap Grad 2 bis 3` | `Dekubitus` |
| `Ulcus Dekubitus` | `Dekubitus` |
| `Ulcus dekubitus` | `Dekubitus` |
| `Ulcus Dekubitus Bereich OS Sacrum` | `Dekubitus` |
| `Ulcus Dekubitus Epuap Grad 3 / 4` | `Dekubitus` |
| `Ulcus dekubitus Ferse,  Stadium 3 / 4` | `Dekubitus` |
| `Ulcus Dekubitus nach Epuap Grad 2 bis 3` | `Dekubitus` |
| `Ulcus lokal abgegrenzt. belegt könnte ebenso nekrotisch sein` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus mit scheinender Hypergranulation oberhalb der Achillessehne` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus mit Stauung` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus nach Meshgraft (zumindest lässt die Struktur darauf schließen), eventuell ist die Struktur aber einer Unterdrucktherapie geschuldet` | `Postoperative Wunde / Dehiszenz` |
| `Ulcus nach Stich` | `Traumatische Wunde` |
| `Ulcus unbekannter Herkunft, könnte traumatologisch bedingte Wunde sein, durch die Wunde bei unsachgemäßer Versorgung entstehen ulcerationen ebenfalls, nicht immer Krankheitsbedingt` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus unklarer Genese` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus unklarer Genese am Bein genaue Lokalisation nicht beurteilbar` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus unklarer Genese, könnte diabet. Ulcus sein, möglich ebenso durch traumatologische Ursachen` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus unklarer Genese, könnte Venös oder arteriell oder mixum sein.
Beachte kleine Nekrose an der Ferse plantar` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus Ursache nicht genau definierbar` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus, bei vermutetem Diabetes` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus, durch die Mangelernährung ( keine Durchblutung) im Wundgebiet  könnte es sich um einen Dekubitus oder ulcus cruris handeln.` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus, Lokalisation am Bein nicht genau definierbar` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus. Ursache klären sollte es ein diabet. Fuß sein dann Prüfung ob angiopathisch oder neuropathisch,
Druckentlastung und Ursachenbeseitigung.` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulkus an der Ferse, warsch. Dekubitus nach EPUAP  Stadium 3` | `Dekubitus` |
| `Ulkus Dekubitus am Os sacrum  nach Epuap Grad 2 / 3` | `Dekubitus` |
| `Verbrennung 2 und 3 Grades nach 9 er Regel etwa 9 % Körperoberfläche` | `Verbrennungswunde` |
| `Verbrennung 2. Grades am Bein` | `Verbrennungswunde` |
| `Verbrennung 2. und teilweise 3. Grades Oberfläche ca 9 %` | `Verbrennungswunde` |
| `Verbrennung Grad 1 bis 2 am rechten Fuß` | `Verbrennungswunde` |
| `Verbrennungswunde 1. bis 2. Grades` | `Verbrennungswunde` |
| `Verbrennungswunde am Arm Grad 2` | `Verbrennungswunde` |
| `vermutlich Mischulcus am rechten Bein, höhe der Knöchel.
Semizirkulär` | `Ulcus cruris mixtum` |
| `Wunde am li Fußrücken mit Sehnenfreilegung` | `Wunde am li Fußrücken mit Sehnenfreilegung` |
| `Wunde aufgrund einer Infusion, welche ins umliegende Gewebe ausgetreten ist` | `Wunde aufgrund einer Infusion, welche ins umliegende Gewebe ausgetreten ist` |
| `zirkuläres Ulcus Unterschenkel (vermutlich Mischulcus)` | `Ulcus cruris mixtum` |


### 1.LOKALISATION_GT_MAPPING

**Anzahl Einträge:** 134

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `...stark exsudierendes, nekrotisch belegtes Ulcus mit grünlicher Verfärbung typisch für Pseudomonas aeruginosa.` | `Enthaltung / keine Angabe` |
| `?` | `Enthaltung / keine Angabe` |
| `???` | `Enthaltung / keine Angabe` |
| `Abdomen` | `Abdomen` |
| `Abdomen, links` | `Abdomen` |
| `Arm` | `Arm / Hand` |
| `Arm oder Bein??` | `Enthaltung / keine Angabe` |
| `Aussenseitig linke Fußsohle` | `Fuß` |
| `Außenknöchel links` | `Fuß` |
| `Bein` | `Bein` |
| `Bein nicht genau definierbar` | `Bein` |
| `Bein wo genau fraglich` | `Bein` |
| `Bein, evtl. links, Unterschenkel` | `Bein` |
| `Bein, evtl. rechts, Unterschenkel` | `Bein` |
| `Bein, genaue Definition nicht möglich` | `Bein` |
| `Bein, genauere Lokalisation nicht genau definierbar` | `Bein` |
| `Bein, Unterschenkel Richtung Fuß` | `Bein` |
| `Bein, wo genau nicht definierbar` | `Bein` |
| `chronisches Ulkus im Bereich der Achillessehne
dorsaler Unterschenkel / Achillessehnenregion` | `Bein` |
| `Das Bild zeigt ein großflächiges venöses Ulcus cruris bei ausgeprägter chronisch venöser Stauung und Adipositas-assoziierter Belastung. Möglich, Oberschenkel links, Unterschenkel` | `Bein` |
| `Ferse` | `Fuß` |
| `Ferse, Achillessehne` | `Fuß` |
| `ferse, fußsohle` | `Fuß` |
| `Ferse, linker Fuß` | `Fuß` |
| `Ferse, rechter Fuß` | `Fuß` |
| `Ferse, scheint links zu sein:
gelblich-fibrinösem Belag
mäßiger Exsudation
gerötetem Wundrand` | `Fuß` |
| `fibrinösem gelblich-weißem Belag,
mäßiger Exsudation,
gerötetem Wundrand,
--> vermutlich entzündlicher bzw. kritisch kolonisierter Situation,` | `Enthaltung / keine Angabe` |
| `Fuß lateral links` | `Fuß` |
| `Fuß links plantar` | `Fuß` |
| `Fuß links plantar  lateral` | `Fuß` |
| `Fuß rechts` | `Fuß` |
| `Fuß, Ferse links` | `Fuß` |
| `Fußrücken` | `Fuß` |
| `Fußrücken linker Fuß` | `Fuß` |
| `Fußrücken rechter Fuß` | `Fuß` |
| `Fußsohle Ferse` | `Fuß` |
| `Gesäß-/perianale Region eines Säuglings` | `Gesäß / Sakral` |
| `Gesäß-/Sakralregion` | `Gesäß / Sakral` |
| `größeres, flächiges Ulcus am Unterschenkel (Wade) bei ausgeprägtem Ödem und Adipositas-assoziierter Hautveränderung.` | `Bein` |
| `keine Angabe möglich` | `Enthaltung / keine Angabe` |
| `Knöchelinnenseite` | `Fuß` |
| `könnte am linken Fuß sein... Knöchelbereich` | `Fuß` |
| `könnte der Unterschenkel sein, rechts` | `Bein` |
| `könnte Innenseite linker Fuß sein` | `Fuß` |
| `könnte oberhalb des os sacrum liegen` | `Gesäß / Sakral` |
| `könnte sich im Bereich des Steißes befinden` | `Gesäß / Sakral` |
| `könnte Unterschenkel oder Handgelenk sein` | `Enthaltung / keine Angabe` |
| `lateral linker Fuß` | `Fuß` |
| `li lateraler Malleolus` | `Fuß` |
| `li. Fußrücken` | `Fuß` |
| `linke Ferse` | `Fuß` |
| `linker Fuss` | `Fuß` |
| `linker Fussrücken` | `Fuß` |
| `linker Fuß` | `Fuß` |
| `linker Fuß
Lokalisation: dorsaler und lateraler Vorfuß mit Beteiligung der Zehenbasis` | `Fuß` |
| `linker Fuß - dorsaler Vorfuß/Fußrücken` | `Fuß` |
| `linker Fuß außen` | `Fuß` |
| `linker Fuß lateratl` | `Fuß` |
| `linker Fuß medial, malleolär` | `Fuß` |
| `linker Fuß medial-lateral 
kleine Nekrose an der Ferse außen plantar` | `Fuß` |
| `linker Fuß, Außenseite` | `Fuß` |
| `linker Fuß, außenseite` | `Fuß` |
| `linker Fuß, Ferse` | `Fuß` |
| `linker Fuß, Innenseite` | `Fuß` |
| `linker Fuß, Mittelfußsohle, Ferse` | `Fuß` |
| `linker Fuß, seite` | `Fuß` |
| `linker Fuß, Spann, Fußrücken` | `Fuß` |
| `linker Fußrücken` | `Fuß` |
| `linker Oberarm, Innenseite` | `Arm / Hand` |
| `linker Oberarm/ Innenseitig` | `Arm / Hand` |
| `linker proximaler Unterschenkel lateral` | `Bein` |
| `linkes Bein unterhalb Knie lateral` | `Bein` |
| `lokalisation nicht genau zu definieren` | `Enthaltung / keine Angabe` |
| `Lokalisation: Fußrücken, lateraler Vorfuß sowie Zehenbereiche` | `Fuß` |
| `Lokalisation: lateraler Mittelfuß/Knöchelbereich` | `Fuß` |
| `Lokalisation: lateraler Vor-/Mittelfuß` | `Fuß` |
| `Lokalisation: sakrogluteale/perianale Region beidseits` | `Gesäß / Sakral` |
| `Lokalisation: Unterschenkelbereich` | `Bein` |
| `Lokalisation: Unterschenkelregion` | `Bein` |
| `Lokalisation: vermutlich Sakral-/Gesäßregion` | `Gesäß / Sakral` |
| `mediale Fußseite linker Fuß` | `Fuß` |
| `mehrere kleine bis mittelgroße Ulzerationen am Unterschenkel (Wade, rechts?) mit entzündlich wirkender Umgebungshaut.` | `Bein` |
| `multiple Schädigung gesamter Gesäßbereich` | `Gesäß / Sakral` |
| `nicht beurteilbar` | `Enthaltung / keine Angabe` |
| `nicht genau definierbar` | `Enthaltung / keine Angabe` |
| `nicht genau definierbar könnte Sakralbereich sein` | `Gesäß / Sakral` |
| `nicht genau definierbar sieht für mich aus wie am Vorfuß` | `Fuß` |
| `nicht genau definierbar, meist am Unterschenkel` | `Bein` |
| `nicht genau definierbar, Vermutung Unterschenkel` | `Bein` |
| `Oberarb Muskulus bizeps` | `Arm / Hand` |
| `oberhalb der Achillessehne` | `Fuß` |
| `Os Sacrum` | `Gesäß / Sakral` |
| `plantarseitig rechter Fuß` | `Fuß` |
| `re Fuß` | `Fuß` |
| `rechte Ferse` | `Fuß` |
| `rechte Hand` | `Arm / Hand` |
| `rechte Hand und Arm` | `Arm / Hand` |
| `rechter Fuß` | `Fuß` |
| `rechter Fuß - lateraler und plantarer Fußbereich/Ferse` | `Fuß` |
| `rechter Fuß Fußrücken und lateral` | `Fuß` |
| `rechter Fuß medial, Richtung plantar.` | `Fuß` |
| `rechter Fuß plantar` | `Fuß` |
| `rechter Fuß, Ferse` | `Fuß` |
| `rechter Fuß, Ferse, Mittelfuß - Fußsohle` | `Fuß` |
| `rechter Fuß, Fußsohle` | `Fuß` |
| `rechter Fuß, in Höhe der großen Zehe, unterhalb der medialen Malleolen` | `Fuß` |
| `rechter Fuß, Innenseite, Knöchel` | `Fuß` |
| `rechter Fuß, Spann` | `Fuß` |
| `rechter Unterarm, rechtes Handgelenk, rechte Hand` | `Arm / Hand` |
| `rechter Unterschenkel` | `Bein` |
| `rechtes Bein, höhe der Knöchel` | `Bein` |
| `rechtes Bein, Kniebereich, Unterschenkel` | `Bein` |
| `Rima Ani` | `Gesäß / Sakral` |
| `sacralbereich` | `Gesäß / Sakral` |
| `Sakralbereich` | `Gesäß / Sakral` |
| `Sakralbereich linke hälfte` | `Gesäß / Sakral` |
| `Sakraler Bereich` | `Gesäß / Sakral` |
| `sakrales Dekubitalulkus` | `Gesäß / Sakral` |
| `schwer zu beurteilen, keine genaue Angabe möglich,
eventuell Rücken Richtung Oberarm /` | `Enthaltung / keine Angabe` |
| `schwer zu beurteilen, Vermutung am Trochanter major` | `Bein` |
| `schwierig zu beantworten... könnte die Wade sein, evtl. rechts` | `Bein` |
| `Steiß` | `Gesäß / Sakral` |
| `Unterarm` | `Arm / Hand` |
| `Unterschenkel` | `Bein` |
| `unterschenkel` | `Bein` |
| `Unterschenkel  medial` | `Bein` |
| `Unterschenkel warsch. gamaschenartig / bereits zirkulierend` | `Bein` |
| `Unterschenkel weit umfassend` | `Bein` |
| `Unterschenkel, Außenseite auf Knie Höhe` | `Bein` |
| `Unterschenkel, rechts, Innenseite` | `Bein` |
| `Unterschenkel/Knöchelregion, zirkumferenziell ausgedehnt` | `Bein` |
| `Unterschenkel?` | `Bein` |
| `vermutlich am Außenknöchel` | `Fuß` |
| `vermutlich am Unterschenkel` | `Bein` |


### 1.EXSUDAT_GT_MAPPING

**Anzahl Einträge:** 62

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Annahme stark` | `Stark` |
| `blutig bis serös teilweise vorhanden dann eher mäßig` | `Mäßig` |
| `eher schwach b is mäßig` | `Leicht`, `Mäßig` |
| `eher wenig` | `Leicht` |
| `eher weniger` | `Leicht` |
| `gering bis gar nicht` | `Keine`, `Leicht` |
| `Große Wunde: stark, da Mazerationen am Wundrand
Kleine Nekrose: trocken` | `Stark` |
| `kein` | `Keine` |
| `Keine` | `Keine` |
| `keine` | `Keine` |
| `keine Angabe möglich` | `Enthaltung / keine Angabe` |
| `keine Angabe möglich / eher wenig` | `Leicht` |
| `keine Angabe möglich / vermutlich mässig` | `Mäßig` |
| `keine Angabe möglich / vermutlich wenig` | `Leicht` |
| `keine Angabe möglich, vermutlich gering` | `Leicht` |
| `keine Angabe möglich, vermutlich trocken` | `Keine` |
| `keine Einschätzung möglich` | `Enthaltung / keine Angabe` |
| `keine genaue Angabe möglich, sieht eher trocken bis leicht exsudierend aus` | `Keine`, `Leicht` |
| `könnte eher schwach sein` | `Leicht` |
| `Leicht` | `Leicht` |
| `leicht` | `Leicht` |
| `leicht bis mittel` | `Leicht`, `Mäßig` |
| `leicht bis mäßig` | `Leicht`, `Mäßig` |
| `leichte bis mäßige exsudation` | `Leicht`, `Mäßig` |
| `mittel` | `Mäßig` |
| `mittel bis stark` | `Mäßig`, `Stark` |
| `mittelstark` | `Mäßig` |
| `mäfig` | `Mäßig` |
| `Mässig` | `Mäßig` |
| `Mäßig` | `Mäßig` |
| `mäßig` | `Mäßig` |
| `mäßig bis stark` | `Mäßig`, `Stark` |
| `mäßig bis stark, sicher ist eine Geruchsbildung süßlich aromatisch teilweise beschrieben als traubenartig` | `Mäßig`, `Stark` |
| `Nekrosen: kein Exsudat. Unterschenkel mäßig` | `Mäßig` |
| `nicht beurteilbar` | `Enthaltung / keine Angabe` |
| `nicht beurteilbar, vermutlich stark` | `Stark` |
| `nicht genau definierbar, aus der Erfahrung heraus mäßige Exsudation` | `Mäßig` |
| `nicht klar, eher trübe Wunde könnte Geruch abgeben` | `Enthaltung / keine Angabe` |
| `nicht zu beschreiben` | `Enthaltung / keine Angabe` |
| `offenen stelle mäßig, geschlossene stelle kein bis wenig exsudat` | `Keine`, `Leicht` |
| `scheint mäßig zu sein` | `Mäßig` |
| `schwach` | `Leicht` |
| `schwach bin mäßig` | `Leicht`, `Mäßig` |
| `schwach bis mäßig` | `Leicht`, `Mäßig` |
| `schwach bis nicht vorhanden` | `Keine`, `Leicht` |
| `sehr gering` | `Leicht` |
| `Stark` | `Stark` |
| `stark` | `Stark` |
| `vermutlich gering` | `Leicht` |
| `vermutlich hoch` | `Stark` |
| `vermutlich hohe Exsudation` | `Stark` |
| `vermutlich kaum` | `Keine` |
| `vermutlich mittel` | `Mäßig` |
| `vermutlich mittelmässig` | `Mäßig` |
| `vermutlich mittelmäßig` | `Mäßig` |
| `vermutlich mässig` | `Mäßig` |
| `vermutlich mäßig` | `Mäßig` |
| `vermutlich starke Exsudation` | `Stark` |
| `vermutlich vorhanden, in welcher Menge ist nicht zu beurteilen` | `Enthaltung / keine Angabe` |
| `vermutlich wenig` | `Leicht` |
| `wahrscheinlich mittelmäßig vorhanden` | `Mäßig` |
| `warsch hoch bis sehr hoch,  klare exsudation` | `Stark` |


### 1.WUNDUMGEBUNG_GT_MAPPING

**Anzahl Einträge:** 38

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `["atrophisch-trockene Haut mit trophischen Störungen","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)` |
| `["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)","Erythem / Rötung"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Erythem / Rötung` |
| `["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)` |
| `["Ekzem / Dermatitis","Erythem / Rötung"]` | `Ekzem / Dermatitis`, `Erythem / Rötung` |
| `["Ekzem / Dermatitis"]` | `Ekzem / Dermatitis` |
| `["empfindliche Säuglingshaut mit hoher Feuchtigkeits- und Reibungsbelastung"]` | `Sonstiges` |
| `["Erythem / Rötung","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Erythem / Rötung` |
| `["Erythem / Rötung","deutliche entzündliche Rötung der Umgebung"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","eher trocken wirkende Umgebung"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","Ekzem / Dermatitis","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Ekzem / Dermatitis`, `Erythem / Rötung` |
| `["Erythem / Rötung","Ekzem / Dermatitis"]` | `Ekzem / Dermatitis`, `Erythem / Rötung` |
| `["Erythem / Rötung","entzündliche Umgebungshaut"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","leicht gerötete, glänzende Umgebungshaut"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","Mazeration","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Erythem / Rötung`, `Mazeration` |
| `["Erythem / Rötung","Mazeration"]` | `Erythem / Rötung`, `Mazeration` |
| `["Erythem / Rötung","Weichteilreizung"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","Ödem","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Erythem / Rötung`, `Ödem` |
| `["Erythem / Rötung","Ödem"]` | `Erythem / Rötung`, `Ödem` |
| `["Erythem / Rötung"]` | `Erythem / Rötung` |
| `["fragile, atrophe Haut"]` | `Sonstiges` |
| `["gerötet-glänzende Haut, Hinweis auf chronische venöse Stauung/Ödemneigung"]` | `Erythem / Rötung`, `Ödem` |
| `["gerötet-glänzende, ödematöse Haut","Erythem / Rötung"]` | `Erythem / Rötung`, `Ödem` |
| `["gut durchbluteter, überwiegend roter Wundgrund"]` | `Reizlos / intakt` |
| `["Keratosen"]` | `Sonstiges` |
| `["Mazeration","Erythem / Rötung","trockener wirkende Areale mit verminderter Durchblutung"]` | `Erythem / Rötung`, `Mazeration` |
| `["Mazeration","Erythem / Rötung"]` | `Erythem / Rötung`, `Mazeration` |
| `["Mazeration","glänzend"]` | `Mazeration` |
| `["Mazeration","glänzende, gespannte Umgebungshaut"]` | `Mazeration` |
| `["Mazeration"]` | `Mazeration` |
| `["Reizlos / intakt","Erythem / Rötung"]` | `Erythem / Rötung`, `Reizlos / intakt` |
| `["Reizlos / intakt"]` | `Reizlos / intakt` |
| `["rocken, teils schuppig, gespannt"]` | `Sonstiges` |
| `["zahlreiche erythematöse Makulae/Papeln, livid-entzündliche Hautveränderungen, Hinweis auf entzündlich-vaskulären Prozess"]` | `Ekzem / Dermatitis`, `Erythem / Rötung` |
| `["Ödem","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Ödem` |
| `["Ödem","Erythem / Rötung"]` | `Erythem / Rötung`, `Ödem` |
| `["Ödem","gespannte, trophisch veränderte Haut"]` | `Ödem` |
| `["Ödem"]` | `Ödem` |
| `[]` |  |


### 1.WUNDRAND_GT_MAPPING

**Anzahl Einträge:** 33

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `["Epibolie (eingerollter Wundrand)","Gerötet / entzündlich","Mazeriert"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich`, `Mazeriert` |
| `["Epibolie (eingerollter Wundrand)","Gerötet / entzündlich"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich` |
| `["Epibolie (eingerollter Wundrand)","Mazeriert"]` | `Epibolie (eingerollter Wundrand)`, `Mazeriert` |
| `["Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)` |
| `["Gelbliche fibrinöse Randbeläge"]` |  |
| `["Gerötet / entzündlich","Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","glänzende, ödematöse Haut"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","livid-erythematöse Hautveränderungen"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","Mazeriert","Unterminiert (Wundtaschen)"]` | `Gerötet / entzündlich`, `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Gerötet / entzündlich","Mazeriert"]` | `Gerötet / entzündlich`, `Mazeriert` |
| `["Gerötet / entzündlich","relativ scharf begrenzte Wundränder"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","Taschenbildung möglich"]` | `Gerötet / entzündlich`, `Unterminiert (Wundtaschen)` |
| `["Gerötet / entzündlich","unregelmäßige Wundränder"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","unregelmäßigen Rändern"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","Unterminiert (Wundtaschen)"]` | `Gerötet / entzündlich`, `Unterminiert (Wundtaschen)` |
| `["Gerötet / entzündlich"]` | `Gerötet / entzündlich` |
| `["Hyperkeratotisch","Gerötet / entzündlich"]` | `Gerötet / entzündlich`, `Hyperkeratotisch` |
| `["Hyperkeratotisch"]` | `Hyperkeratotisch` |
| `["Mazeriert","Epibolie (eingerollter Wundrand)","Gerötet / entzündlich"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich`, `Mazeriert` |
| `["Mazeriert","Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)`, `Mazeriert` |
| `["Mazeriert","Gerötet / entzündlich","Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich`, `Mazeriert` |
| `["Mazeriert","Gerötet / entzündlich","Unterminiert (Wundtaschen)"]` | `Gerötet / entzündlich`, `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Mazeriert","Gerötet / entzündlich"]` | `Gerötet / entzündlich`, `Mazeriert` |
| `["Mazeriert","teilweise aufgequollen"]` | `Mazeriert` |
| `["Mazeriert","Unterminiert (Wundtaschen)","Gerötet / entzündlich"]` | `Gerötet / entzündlich`, `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Mazeriert","Unterminiert (Wundtaschen)"]` | `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Mazeriert"]` | `Mazeriert` |
| `["Reizlos / unauffällig"]` | `Reizlos / unauffällig` |
| `["scharf begrenzt, teils livide/verfärbt, ischämietypisch"]` | `Reizlos / unauffällig` |
| `["Unterminiert (Wundtaschen)","Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)`, `Unterminiert (Wundtaschen)` |
| `["Unterminiert (Wundtaschen)","Gerötet / entzündlich"]` | `Gerötet / entzündlich`, `Unterminiert (Wundtaschen)` |
| `["Unterminiert (Wundtaschen)","Mazeriert"]` | `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Unterminiert (Wundtaschen)"]` | `Unterminiert (Wundtaschen)` |


### 1.SEKUNDAERVERBAND_GT_MAPPING

**Anzahl Einträge:** 53

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `abhängig von der Druckentlastung` | `abhängig von Druckentlastung` |
| `abhängig von der Kompressionstherapie` | `abhängig von Kompressionstherapie` |
| `abhängig von Druckentlastung` | `abhängig von Druckentlastung` |
| `abhängig von Kompressionstherapie` | `abhängig von Kompressionstherapie` |
| `absorbierender Schaumverband` | `Schaumstoffverbände (Foam)` |
| `absorbierender Schaumverband, atraumatische Fixierung` | `Schaumstoffverbände (Foam)` |
| `absorbierender Schaumverband, Superabsorber bei stärkerer Sekretion` | `Schaumstoffverbände (Foam)`, `Superabsorber` |
| `atraumatische Schaumverbände` | `Schaumstoffverbände (Foam)` |
| `atraumatische Schaumverbände, ggf. Unterdrucktherapie (VAC) nach Débridement` | `Schaumstoffverbände (Foam)` |
| `atraumatischer Schaumverband` | `Schaumstoffverbände (Foam)` |
| `dünner PU-Schaumverband` | `Schaumstoffverbände (Foam)` |
| `Elastische Fixierbinden` | `Elastische Fixierbinden` |
| `Elastische Fixierbinden, dünner PU-Schaumverband` | `Schaumstoffverbände (Foam)`, `Elastische Fixierbinden` |
| `Fixierbinden / kohäsive Binden` | `Fixierbinden / kohäsive Binden` |
| `Fixiervlies / -pflaster` | `Fixiervlies / -pflaster` |
| `kleiner PU-Schaumverband oder weicher Superabsorber bei stärkerer Exsudation` | `Schaumstoffverbände (Foam)`, `Superabsorber` |
| `kommt auf die Kompression an` | `abhängig von Kompressionstherapie` |
| `Kompressionstherapie` | `abhängig von Kompressionstherapie` |
| `Nicht erforderlich (selbsthaftender Primärverband)` | `Kein Sekundärverband erforderlich` |
| `PU-Schaumverband` | `Schaumstoffverbände (Foam)` |
| `PU-Schaumverband oder kleiner Superabsorber bei stärkerer Sekretion` | `Schaumstoffverbände (Foam)`, `Superabsorber` |
| `PU-Schaumverband oder Superabsorber` | `Superabsorber`, `Schaumstoffverbände (Foam)` |
| `PU-Schaumverband oder Superabsorber bei stärkerer Exsudation` | `Schaumstoffverbände (Foam)`, `Superabsorber` |
| `PU-Schaumverband, Atraumatische Fixierung` | `Schaumstoffverbände (Foam)` |
| `PU-Schaumverband, bei stärkerem Exsudat: Superabsorber` | `Schaumstoffverbände (Foam)`, `Superabsorber` |
| `PU-Schaumverband, Superabsorber bei stärkerer Sekretion` | `Schaumstoffverbände (Foam)`, `Superabsorber` |
| `saugfähiger Schaumverband` | `Schaumstoffverbände (Foam)` |
| `saugfähiger Schaumverband, atraumatische Fixierung` | `Schaumstoffverbände (Foam)` |
| `Schaumstoffverbände` | `Schaumstoffverbände (Foam)` |
| `Schaumstoffverbände (Foam)` | `Schaumstoffverbände (Foam)` |
| `Schaumverband` | `Schaumstoffverbände (Foam)` |
| `Sekundär: Superabsorber + Fixier-/Kompressionssystem` | `Superabsorber` |
| `silikonisierter Schaumverband, absorbierende sterile Auflagen` | `Schaumstoffverbände (Foam)`, `Sterile Saugkompressen / Polsterung` |
| `silikonisierter Schaumverband, absorbierender PU-Schaumverband` | `Schaumstoffverbände (Foam)` |
| `stark saugfähige Superabsorber` | `Superabsorber` |
| `Sterile Saugkompressen / Polsterung` | `Sterile Saugkompressen / Polsterung` |
| `Superabsorber` | `Superabsorber` |
| `Superabsorber bei stärkerer Sekretion` | `Superabsorber` |
| `Superabsorber ergänzen` | `Superabsorber` |
| `Superabsorber oder PU-Schaumverband` | `Superabsorber`, `Schaumstoffverbände (Foam)` |
| `Superabsorber weicher PU-Schaumverband` | `Superabsorber`, `Schaumstoffverbände (Foam)` |
| `Superabsorber, hochabsorbierende Schaumverbände` | `Superabsorber`, `Schaumstoffverbände (Foam)` |
| `Superabsorber, hochabsorbierender PU-Schaumverband` | `Superabsorber`, `Schaumstoffverbände (Foam)` |
| `Superabsorber-Verband` | `Superabsorber` |
| `weicher absorbierender Schaumverband sterile Saugkompressen` | `Schaumstoffverbände (Foam)`, `Sterile Saugkompressen / Polsterung` |
| `weicher PU-Schaumverband druckreduzierende Polsterung` | `Schaumstoffverbände (Foam)` |
| `weicher PU-Schaumverband Superabsorber bei stärkerem Exsudat` | `Schaumstoffverbände (Foam)`, `Superabsorber` |
| `weicher PU-Schaumverband, druckentlastende Polsterung` | `Schaumstoffverbände (Foam)` |
| `weicher PU-Schaumverband, druckreduzierende Polsterung, ggf. Superabsorber` | `Schaumstoffverbände (Foam)`, `Superabsorber` |
| `weicher PU-Schaumverband, sterile Polsterung` | `Schaumstoffverbände (Foam)`, `Sterile Saugkompressen / Polsterung` |
| `weicher PU-Schaumverband, weicher PU-Schaumverband` | `Schaumstoffverbände (Foam)` |
| `weicher PU-Schaumverband,absorbierende sterile Sekundärauflagen` | `Schaumstoffverbände (Foam)`, `Sterile Saugkompressen / Polsterung` |
| `über Kompression` | `abhängig von Kompressionstherapie` |


### 1.PRODUKT_GT_MAPPING

**Anzahl Einträge:** 43

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Alginate` | `Alginate` |
| `Alginate bei stärker exsudierend` | `Alginate` |
| `Alginate, Hydrofaser / Hydrofiber, bei kritischer Kolonisation silberhaltige Varianten erwägen` | `Hydrofaser / Hydrofiber`, `Alginate` |
| `Alginate, Hydrofaser / Hydrofiber, Superabsorber, ggf. Unterdrucktherapie (NPWT/VAC) nach Nekrosensanierung` | `Alginate`, `Hydrofaser / Hydrofiber`, `Superabsorber` |
| `antimikrobielle Alginate` | `Alginate` |
| `antimikrobielle Alginate ggf. PHMB-haltige Wundauflagen` | `Alginate`, `PHMB-haltige Wundauflagen` |
| `antiseptische Wundauflagen --> Silber PHMB-haltige Produkte` | `PHMB-haltige Wundauflagen` |
| `Bei feuchten/infizierten Bereichen: Silberhydrofaser Silberalginat antimikrobielle Wundauflagen` | `Hydrofaser / Hydrofiber`, `Alginate` |
| `Bei feuchten/infizierten Bereichen: Silberhydrofaser Silberalginat antimikrobielle Wundauflagen.` | `Hydrofaser / Hydrofiber`, `Alginate` |
| `Bei kritischer Kolonisation: Silberhydrofaser kurzfristig` | `Hydrofaser / Hydrofiber` |
| `Bei kritischer Kolonisation: Silberhydrofaser kurzfristig, Hydrogele (Kompresse)` | `Hydrofaser / Hydrofiber`, `Hydrogele (Kompresse)` |
| `Bei trockenen Nekrosen: atraumatische trockene Schutzverbände` | `trockene sterile Schutzverbände` |
| `Bei trockenen Nekrosen: atraumatische trockene Schutzverbände, Bei feuchten/infizierten Bereichen: Silberhydrofaser Silberalginat antimikrobielle Wundauflagen` | `trockene sterile Schutzverbände`, `Hydrofaser / Hydrofiber`, `Alginate` |
| `Bei trockener Nekrose: trockener Schutzverband atraumatische Kontaktlagen.` | `trockene sterile Schutzverbände`, `Wundkontaktschichten (Silikon/Paraffin)` |
| `ggf. Hydrogel bei trockeneren Belägen` | `Hydrogele (Kompresse)` |
| `Hydrofaser / Hydrofiber` | `Hydrofaser / Hydrofiber` |
| `Hydrofaser / Hydrofiber, Bei Infektionsverdacht silberhaltige Varianten, Schaumstoffverbände (Foam)` | `Hydrofaser / Hydrofiber`, `Schaumstoffverbände (Foam)` |
| `Hydrofaser / Hydrofiber, Schaumstoffverbände (Foam), Silber-Schaumverbände` | `Hydrofaser / Hydrofiber`, `Schaumstoffverbände (Foam)` |
| `Hydrofaser / Hydrofiber, silberhaltige Varianten bei bakterieller Belastung` | `Hydrofaser / Hydrofiber` |
| `Hydrofaser / Hydrofiber, Wundkontaktschichten (Silikon/Paraffin), Bei bakterieller Belastung: silberhaltige Varianten kurzfristig` | `Hydrofaser / Hydrofiber`, `Wundkontaktschichten (Silikon/Paraffin)` |
| `Hydrogel bei trockenen Nekroseanteilen, Hydrofaser oder Alginat bei Exsudat` | `Hydrogele (Kompresse)`, `Hydrofaser / Hydrofiber`, `Alginate` |
| `Hydrogele (Kompresse)` | `Hydrogele (Kompresse)` |
| `Hydrokolloide` | `Hydrokolloide` |
| `Hydropolymerverbände` | `Schaumstoffverbände (Foam)` |
| `Lipidokolloid-Auflagen` | `Wundkontaktschichten (Silikon/Paraffin)` |
| `PHMB-haltige Auflagen` | `PHMB-haltige Wundauflagen` |
| `PHMB-haltige Wundauflagen` | `PHMB-haltige Wundauflagen` |
| `Schaumstoffverbände` | `Schaumstoffverbände (Foam)` |
| `Schaumstoffverbände (Foam)` | `Schaumstoffverbände (Foam)` |
| `Schaumstoffverbände (Foam), silberhaltige Verbrennungsauflagen` | `Schaumstoffverbände (Foam)` |
| `Silber-Schaumverbände` | `Schaumstoffverbände (Foam)` |
| `Silberalginat` | `Alginate` |
| `Silberalginat, antimikrobielle Alginate ggf. PHMB-haltige Wundauflagen` | `Alginate`, `PHMB-haltige Wundauflagen` |
| `Silberalginate, Silberhydrofaser` | `Hydrofaser / Hydrofiber`, `Alginate` |
| `Silberhydrofaser` | `Hydrofaser / Hydrofiber` |
| `Silberhydrofaser oder Silberalginat` | `Hydrofaser / Hydrofiber`, `Alginate` |
| `Silberhydrofaser, antimikrobielle Alginate` | `Hydrofaser / Hydrofiber`, `Alginate` |
| `Silberhydrofaser, Silberalginat` | `Hydrofaser / Hydrofiber`, `Alginate` |
| `silberhydrofaser/Silberalginat bei kritischer Kolonisation` | `Hydrofaser / Hydrofiber`, `Alginate` |
| `Superabsorber` | `Superabsorber` |
| `trockene sterile Abdeckung, atraumatische Schutzverbände, keine aggressive Befeuchtung` | `trockene sterile Schutzverbände` |
| `trockene sterile Schutzverbände, atraumatische Kontaktlagen, keine aggressive Befeuchtung der stabilen Nekrose` | `trockene sterile Schutzverbände`, `Wundkontaktschichten (Silikon/Paraffin)` |
| `Wundkontaktschichten (Silikon/Paraffin)` | `Wundkontaktschichten (Silikon/Paraffin)` |


### 1.DEBRIDEMENT_GT_MAPPING

**Anzahl Einträge:** 23

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Autolytisch (Hydrogele, Chirurgisch/Scharf (Skalpell, Folienverbände), Hydrokolloide, Kürette)` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `Autolytisch (Hydrogele, Chirurgisch/Scharf (Skalpell, Folienverbände), Hydrokolloide, Kürette), Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)`, `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `Autolytisch (Hydrogele, Folienverbände), Hydrokolloide` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)` |
| `Autolytisch (Hydrogele, Folienverbände), Hydrokolloide, Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)` |
| `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)` |
| `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette), Enzymatisch` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Chirurgisch/Scharf (Skalpell, Kürette)`, `Enzymatisch (Kollagenase)` |
| `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), chirurgisches Debridement erst nach Perfusionsverbesserung, sofern möglich` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), vorsichtig mechanisches Debridement` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)` |
| `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), vorsichtige mechanische Reinigung lockerer Beläge` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)` |
| `autolytisches Debridement, enzymatisches Debridement - ergänzend` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Enzymatisch (Kollagenase)` |
| `Chirurgisch/Scharf (Skalpell, Kürette)` | `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `Chirurgisch/Scharf (Skalpell, Kürette), autolytisches Debridement, enzymatisches Debridement - ergänzend` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Chirurgisch/Scharf (Skalpell, Kürette)`, `Enzymatisch (Kollagenase)` |
| `Chirurgisch/Scharf (Skalpell, Kürette), Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen` | `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)`, `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `chirurgisches Debridement erst nach Perfusionsverbesserung, sofern möglich` | `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `Enzymatisch (Kollagenase)` | `Enzymatisch (Kollagenase)` |
| `kein aggressives Debridement ohne Gefäßstatus, trockene stabile Nekrosen ggf. belassen, Bei infizierten/fibrinösen Belägen: zurückhaltendes scharfes Debridement, autolytische Verfahren möglich` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `Kein Débridement erforderlich` | `Kein Débridement erforderlich` |
| `konservatives Abwarten bei unklarer Demarkation, selektives chirurgisches Débridement, enzymatisch/autolytisch ergänzend` | `Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)`, `Chirurgisch/Scharf (Skalpell, Kürette)`, `Enzymatisch (Kollagenase)` |
| `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)` | `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)` |
| `Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen` | `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)` |
| `nicht aggressiv entfernen, solange keine Revaskularisation erfolgt ist, Chirurgisch/Scharf (Skalpell, Kürette)` | `Chirurgisch/Scharf (Skalpell, Kürette)` |
| `vorsichtig mechanisches Debridement` | `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)` |
| `vorsichtige mechanische Reinigung lockerer Beläge` | `Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)` |


### 1.SPUELLOESUNG_GT_MAPPING

**Anzahl Einträge:** 10

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` | `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` |
| `Antimikrobielle Spüllösung (PHMB, Octenisept)` | `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` |
| `Antiseptika nur gezielt bei: Infektionszeichen, kritischer Kolonisation` | `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` |
| `bei kritischer Kolonisation: mit PHMB/Octenidin` | `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` |
| `Bei kritischer Kolonisation: PHMB oder Octenidin zeitlich begrenzt` | `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` |
| `bei kritischer Kolonisation: PHMB oder Octenidin zeitlich begrenzt` | `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` |
| `bei kritischer Kolonisation: PHMB/Octenidin` | `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` |
| `Neutrale Spüllösung (NaCl 0,9 % / Ringer-Lösung)` | `Neutrale Spüllösung (NaCl 0,9 % / Ringer-Lösung)` |
| `Neutrale Spüllösung (NaCl, Ringer)` | `Neutrale Spüllösung (NaCl 0,9 % / Ringer-Lösung)` |
| `PHMB oder Octenidin zeitlich begrenzt` | `Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)` |


### 1.ANTIMIKROBIELL_GT_MAPPING

**Anzahl Einträge:** 6

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Cadexomer-Iod` | `Cadexomer-Iod` |
| `Honig (Medihoney)` | `Honig (Medihoney)` |
| `Octenidin` | `Octenidin` |
| `PHMB` | `PHMB` |
| `Silber (Ag+)` | `Silber (Ag+)` |
| `Silber (Ag⁺)` | `Silber (Ag+)` |


### 1.HAUTSCHUTZ_GT_MAPPING

**Anzahl Einträge:** 4

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Hautschutzfilm / Barrierespray` | `Hautschutzfilm / Barrierespray` |
| `Nicht erforderlich` | `Kein Hautschutz erforderlich` |
| `Wundrandschutzpaste` | `Wundrandschutzpaste` |
| `Zinksalbe / Zinkpaste` | `Zinksalbe / Zinkpaste` |


### 1.KOMPRESSION_GT_MAPPING

**Anzahl Einträge:** 5

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Adaptive Kompressionsbandagen (Wrap)` | `Adaptive Kompressionsbandagen (Wrap)` |
| `Kurzzugbinden` | `Kurzzugbinden` |
| `Medizinische Kompressionsstrümpfe (MKS)` | `Medizinische Kompressionsstrümpfe (MKS)` |
| `medizinische Kompressionssysteme` | `Medizinische Kompressionsstrümpfe (MKS)` |
| `Mehrkomponentensysteme (2-/4-Lagen)` | `Mehrkomponentensysteme (2-/4-Lagen)` |


### 1.LOKALISATION_KEYWORDS

**Anzahl Einträge:** 6

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Abdomen` | `abdomen`, `bauch`, `bauchdecke`, `abdominal` |
| `Arm` | `arm`, `oberarm`, `unterarm` |
| `Bein` | `bein`, `schenkel`, `wade`, `knie`, `achilles`, `knöchelregion`, `unterschenkel`, `gaiter` |
| `Fuß` | `fuß`, `fus`, `ferse`, `knöchel`, `zehe`, `spann`, `sohle`, `plantar`, `vorfuß`, `mittelfuß`, `fußrücken`, `sprunggelenk`, `malleolar`, `malleol`, `dorsolateral`, `dorsalseitig`, `rückfuß`, `großzehe`, `calcaneus`, `außenknöchel` |
| `Gesäß/Steiß` | `gesäß`, `gesaess`, `sakral`, `steiß`, `steiss`, `perianal`, `sakrogluteal`, `gluteal`, `intergluteal`, `leiste`, `leistenregion`, `inguinal` |
| `Hand` | `hand`, `handgelenk` |


### 1.SPELLING_MAPPING

**Anzahl Einträge:** 2

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `decubitus` | `dekubitus` |
| `ulcus` | `ulkus` |


## 2. Lohmann & Rauscher Normalisierungsschema (`mappings_LR.py`)

### 2.WUNDGRUND_GT_MAPPING

**Anzahl Einträge:** 266

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Ausgedehnte gelb-grünliche Fibrin-/Beläge mit Biofilm, teils weich-nekrotische Areale; feucht, keine freiliegenden Strukturen erkennbar.` | `Biofilm`, `Fibrinbelag`, `Nekrose` |
| `Ausgedehnte gelblich-fibrinöse Beläge mit schwarz-braunen Nekrosen, dazwischen rötliche granulierende Areale; feucht-glänzend.` | `Fibrinbelag`, `Nekrose`, `Rötung`, `Granulation` |
| `Ausgedehnte livid‑violette Hautverfärbung mit deutlicher Schwellung; multiple intakte und kollabierte Blasen (teils serös/serosanguinös gefüllt); oberflächliche Erosionen/Krusten in rechteckigen Arealen; keine sichtbare Granulation, kein freiliegendes tiefes Gewebe erkennbar.` | `Blasenbildung` |
| `Ausgedehnte schwarz-braune Nekrose/Eschar mit feucht-glänzender Oberfläche, teils fibrinös belegt; keine Granulation sichtbar.` | `Nekrose`, `Fibrinbelag` |
| `Ausgedehnte schwarz-braune Nekrosen mit gelblich-fibrinösen Belägen; zentral rötlich-granulierende Anteile; unregelmäßiger, teils tiefer Defekt.` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Ausgedehnte schwarze trockene Nekrose am unteren Ulkus, oberes Ulkus mit gelblichen Fibrinbelägen; kein Granulationsgewebe sichtbar.` | `Fibrinbelag`, `Nekrose` |
| `Ausgedehnter gelb-grünlicher Fibrin-/Detritusbelag mit einzelnen nekrotischen Arealen, kaum Granulation sichtbar; oberflächlich bis flach, unregelmäßige Ränder.` | `Fibrinbelag`, `Nekrose` |
| `ausgedehnter gelblich-fibrinöser Belag/Biofilm mit einzelnen rötlich-granulierenden Anteilen; feucht` | `Biofilm`, `Fibrinbelag`, `Granulation` |
| `Ausgedehnter schwarz-brauner Nekroseanteil mit gelblich-grünem Fibrin/Slough, feucht glänzend; möglicher Biofilm` | `Biofilm`, `Fibrinbelag`, `Nekrose` |
| `belegt mit Hypergranulation` | `Hypergranulation` |
| `belegt, fibrinös, nekrotisch` | `Fibrinbelag`, `Nekrose` |
| `belegt, hypergranulation` | `Belag`, `Hypergranulation` |
| `belegt, mäßige Exsudation Infektion möglich` | `Belag`, `Exsudat` |
| `belegt, nekrotisch` | `Belag`, `Nekrose` |
| `belegt, teilweise kleine Nekrosen freiliegende Sehne sichtbar` | `Belag`, `Nekrose`, `Freiliegende Sehnen` |
| `belegt, teilweise kleine Nekrosen, könnte infiziert sein` | `Belag`, `Nekrose` |
| `belegt, teilweise kleine Nekrosen, könnte infiziert sein, belegt` | `Belag`, `Nekrose` |
| `belegt, teilweise nekrotisch` | `Belag`, `Nekrose` |
| `belegt, teilweise nekrotisch könnte infiziert sein` | `Belag`, `Nekrose` |
| `belegt, teilweise nekrotisch, teilweise überschießende Granulation` | `Belag`, `Nekrose`, `Hypergranulation` |
| `belegte Wunde, teilweise infiziert` | `Belag`, `Infektion` |
| `Drei rund-ovale, teils tief reichende Defekte mit zentral schwarz-brauner Nekrose (Eschar) und gelblich-weißen fibrinösen Belägen; feucht-glänzende Oberfläche; am Rand abschnittsweise rötliches Granulationsgewebe erkennbar.` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Exsudation` | `Exsudat` |
| `Feucht glänzender, teils gelblich fibrinös belegter Wundgrund mit fragiler Granulation, oberflächlich, keine erkennbaren Taschen.` | `Fibrinbelag`, `Granulation` |
| `Feucht-glänzender Wundgrund mit flächigen, gelblich-weißen fibrinösen Belägen/Slough und vereinzelten rötlichen Granulationsinseln; keine schwarze Nekrose erkennbar; keine freiliegenden Sehnen/Knochen.` | `Fibrinbelag`, `Granulation` |
| `feuchte Nekrose,` | `Nekrose` |
| `Feuchtes, gut durchblutetes granulierendes Wundbett mit kleinen, fest anhaftenden fibrinösen Inseln/Belägen; kein nekrotisches Gewebe sichtbar.` | `Granulation`, `Fibrinbelag` |
| `Feuchtes, teils granulierendes Wundbett mit ausgeprägten gelb-weißlichen Fibrinbelägen; keine trockene Nekrose erkennbar.` | `Granulation`, `Fibrinbelag` |
| `Fibrinbelegt` | `Fibrinbelag` |
| `Fibrinbelegt bei Wundrandepithelisierung` | `Fibrinbelag`, `Wundrandepithelisierung` |
| `Fibrinbelegt mit einzelnen Granulationsinseln` | `Fibrinbelag`, `Granulation` |
| `Fibrinbelegt, zerklüftet` | `Fibrinbelag`, `Zerklüftet` |
| `Fibrinbelegte Wunde` | `Fibrinbelag` |
| `Fibrinbelegte Wundverhältnisse` | `Fibrinbelag` |
| `Fibrinbelegtes tiefes Ulcus` | `Fibrinbelag`, `Ulzeration` |
| `Fibringbelegt mit durschscheinendem Granulationsgewebe` | `Fibrinbelag`, `Granulation` |
| `fibrinös belegt, unterminierte Wundränder siehe punktierte Markierung
Eventuelle freie Sehnen` | `Fibrinbelag`, `Unterminierung`, `Freiliegende Sehnen` |
| `fibrinös belegt, zum Teil mit Granulationsinseln, teilweise freiliegende Sehnen.
Nekrose plantar wandständig trocken` | `Fibrinbelag`, `Granulation`, `Freiliegende Sehnen`, `Nekrose` |
| `Fibrinös-gelblicher Belag mit Inseln rötlicher Granulation; feucht, keine trockene Nekrose sichtbar.` | `Fibrinbelag`, `Rötung`, `Granulation` |
| `Flache, ovale Ulzeration mit zentral gelblichen Fibrinbelägen; randständig rötliche, feuchte Granulation.` | `Ulzeration`, `Fibrinbelag`, `Granulation`, `Rötung` |
| `Flacher Defekt mit überwiegender roter Granulation und teils gelblich-fibrinösen Belägen; keine trockene Nekrose sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Flacher, ausgedehnter Defekt mit rötlich granulierendem Gewebe und ausgedehnten gelblich-fibrinösen Belägen; stark feucht/glänzend; keine schwarze Nekrose sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Flaches Ulkus mit gelblich-fibrinösen Belägen und Anteilen von Granulationsgewebe; feucht.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Flaches, irreguläres Ulkus mit gelblich-fibrinösen Belägen und Anteilen von Granulationsgewebe; feucht.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Flaches, ovales Ulkus mit überwiegend gelblich-beigem Fibrinbelag; feucht glänzend; keine schwarzen Nekrosen und keine freiliegenden tiefen Strukturen sichtbar.` | `Ulzeration`, `Fibrinbelag` |
| `fleischige Wunde mit Taschenbildung nach Feststellung der Ausdehnung` | `Granulation`, `Taschenbildung` |
| `Flächendeckende, zähe gelblich-weiße Fibrinbeläge/Slough (~80%) mit geringen granulierenden Inseln; feucht; keine schwarze Nekrose; unregelmäßige Wundtiefe.` | `Fibrinbelag`, `Granulation` |
| `Flächig erythematös-erosiv, teils mit weißlich-schuppigen Auflagerungen; kein nekrotisches Gewebe erkennbar; feucht-glänzend; mäßige Exsudation.` | `Rötung`, `Exsudat` |
| `Flächig oberflächlich erosiv, feucht glänzend mit teils fibrinösen Belägen und rötlich-granulierenden Arealen.` | `Fibrinbelag`, `Granulation` |
| `freiliegende Sehnen Strang 5, freiliegende Knochen,
teilweise nekrotisch` | `Freiliegende Sehnen`, `Freiliegende Knochen`, `Nekrose` |
| `Fußwunde: Nekrotisch  Unterschenkelwunde fibrinös belegt,` | `Nekrose`, `Fibrinbelag` |
| `Gelb-beiger, feuchter fibrinöser Belag/flächiger Slough, kaum Granulation sichtbar.` | `Fibrinbelag` |
| `Gelb-bräunliche Fibrinauflagerungen mit zentralen schwarz-braunen Nekroseanteilen; kein Granulationsgewebe sichtbar.` | `Fibrinbelag`, `Nekrose` |
| `Gelb-grauer fibrinöser Belag mit feuchtem Slough; Tiefe/Unterminierungen nicht sicher beurteilbar.` | `Fibrinbelag`, `Taschenbildung` |
| `Gelb-grünlicher Fibrinbelag mit zentraler schwarz-brauner Nekrose; feucht erscheinend.` | `Fibrinbelag`, `Nekrose` |
| `Gelb-ockerfarbener, fest anhaftender Fibrin-/Nekrosebelag mit zentral dunklen (schwarz-braunen) Nekroseinseln; keine sichtbare Granulation; Oberfläche teils krustös, teils feucht glänzend.` | `Fibrinbelag`, `Nekrose` |
| `Gelb-weißliche fibrinöse Beläge mit rötlich granulierenden Arealen; feuchter Wundgrund.` | `Fibrinbelag`, `Granulation` |
| `Gelb-weißlicher fibrinöser Belag mit zentral dunkler nekrotischer Komponente; bislang kaum Granulation sichtbar.` | `Fibrinbelag`, `Nekrose` |
| `Gelblich-beiger, feuchter Fibrinbelag/Slough (~70%) mit randständiger rötlicher Granulation (~30%); keine schwarze Nekrose sichtbar.` | `Fibrinbelag`, `Rötung`, `Granulation` |
| `gelblich-brauner Fibrinbelag mit teils rötlichen Anteilen; keine freiliegenden Strukturen sichtbar` | `Fibrinbelag` |
| `Gelblich-fibrinös belegter, feucht-glänzender Wundgrund mit teils rötlichen Arealen; kein trockener Nekroseanteil sichtbar.` | `Fibrinbelag`, `Rötung` |
| `gelblich-fibrinös belegter, teils nekrotischer Wundgrund mit Ulkuskrater; zweite Läsion mit trockener Nekrose/Schorf` | `Fibrinbelag`, `Nekrose` |
| `Gelblich-grünlicher Fibrin-/Belag mit teils rötlich punktförmig granulierenden Arealen; oberflächliche, irreguläre Ulzera.` | `Fibrinbelag`, `Granulation` |
| `Gelblich-weißer, zäher fibrinöser Belag mit wenigen punktförmigen Blutungen; feucht, vereinzelte rötliche Areale.` | `Fibrinbelag`, `Rötung` |
| `Gelbliche fibrinöse Beläge, teils granulierend; flach-kraterförmiger Defekt.` | `Fibrinbelag`, `Granulation` |
| `Gelblicher, zäher Fibrinbelag; kaum Granulation; teils tieferliegendes Gewebe/Faszie sichtbar.` | `Fibrinbelag` |
| `Gelb‑bräunlicher Fibrinbelag mit zentralen schwarz‑nekrotischen Arealen; kaum/keine sichtbare Granulation.` | `Fibrinbelag`, `Nekrose` |
| `Gemischt: gelblich-fibrinöse Beläge mit Anteilen von feuchter Granulation; unregelmäßige, flach bis mäßig tiefe Läsion.` | `Fibrinbelag`, `Granulation` |
| `Gemischt: überwiegend rote Granulation mit teils gelblich-fibrinösen Belägen; feuchter Wundgrund.` | `Rötung`, `Granulation`, `Fibrinbelag` |
| `Gemischter Wundgrund mit gelb-grünlichen Fibrinbelägen und teils schwarzer trockener Nekrose; teilweise gerötete, leicht feuchte Umgebung; geringe Blutungsspuren` | `Fibrinbelag`, `Nekrose` |
| `Gemischter Wundgrund mit gelb-weißen Fibrinbelägen und dazwischen vitalem Granulationsgewebe; feucht, oval.` | `Fibrinbelag`, `Granulation` |
| `Gemischter Wundgrund mit gelblichen fibrinösen Belägen/Slough und rötlichem Granulationsgewebe; feucht, mäßige Tiefe; kein freiliegender Knochen sichtbar.` | `Fibrinbelag`, `Rötung`, `Granulation` |
| `Gemischter Wundgrund mit rötlicher, feucht glänzender Granulation und ausgedehnten gelblich-fibrinösen Belägen; flach und unregelmäßig, teils zusammenfließende Ulzerationen; keine schwarze Nekrose sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Gemischter Wundgrund: großflächige schwarz-braune Nekrosen/Eschar und gelb-grauer Fibrinbelag; zentral tieferer Defekt mit rötlichem, feuchtem Granulationsgewebe; unregelmäßig, teilweise kavitiert; feucht glänzend; keine exponierten Knochen/Sehnen sichtbar.` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Gemischtes Wundbett mit schwarzen nekrotischen Arealen und gelb-grauem Fibrinbelag; zentral rötliches, feuchtes Granulationsgewebe; tiefe Ulzeration mit möglicher Unterminierung.` | `Nekrose`, `Fibrinbelag`, `Rötung`, `Granulation`, `Ulzeration`, `Unterminierung` |
| `gerötet, stark geschädigt, teilweise nekrotisch belegt` | `Rötung`, `Nekrose`, `Belag` |
| `Granulation und Beläge gleichzeitig` | `Granulation`, `Belag` |
| `Granulationsgewebe, teilweise fibrinös belegt, Biofilm` | `Granulation`, `Fibrinbelag`, `Biofilm` |
| `Granulationsinseln, fibrinös belegt` | `Granulation`, `Fibrinbelag` |
| `Granulierender Wundgrund mit ausgeprägten gelblichen fibrinösen Belägen/Slough, teils adhärent; vereinzelt dunklere nekrotische Areale distal.` | `Granulation`, `Fibrinbelag`, `Nekrose` |
| `Granulierendes Gewebe mit gelblich-fibrinösen Belägen; schräger, mäßig tiefer Defekt mit möglicher Randunterminierung; feucht glänzend.` | `Fibrinbelag`, `Granulation`, `Taschenbildung` |
| `Großes rundes Ulkus mit überwiegend gelblich-weißem Fibrin-/Schleimhautbelag, zentral teils rötliche Granulationsinseln; randständig trockene nekrotische Krusten; feucht-glänzend, kein freiliegender Knochen oder Sehne sichtbar.` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Großes rundes Ulkus mit überwiegend gelblich-weißem Fibrin-/Schleimhautbelag, zentral teils rötliche Granulationsinseln; randständig trockene nekrotische Krusten; feucht-glänzend; kein freiliegender Knochen oder Sehne sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Granulation`, `Nekrose` |
| `großes Ulcus: belegt, teilweise nekrotisch
Zehe: trockene Nekrose- bitte nicht durch autolytisches Débridement anfeuchten. Zeh fällt irgendwann ab, da die Durchblutung massiv gestört ist. Gefäßstatus prüfen und gfls. sanieren` | `Belag`, `Nekrose` |
| `Großflächig flaches Areal mit kräftig rotem, feucht-glänzendem, homogenem Granulationsgewebe; keine sichtbaren Nekrosen oder gelblichen Fibrinbeläge; randständige beginnende Epithelisierung.` | `Granulation`, `Wundrandepithelisierung` |
| `Großflächig gelb‑grünlicher, dicker Fibrin-/Slough-Belag, feucht und glänzend; am unteren Rand schwarz‑braune nekrotische/krustige Areale; nur wenige rötliche Granulationsinseln sichtbar; keine freiliegenden Strukturen (Knochen/Sehnen) erkennbar.` | `Fibrinbelag`, `Nekrose`, `Granulation` |
| `Großflächig nekrotisch mit schwarz-braunen Escharen; darüber ausgedehnter gelb-grünlicher fibrinöser Belag/Slough, feucht-glänzend; keine sichtbare Granulation oder Epithelisierung.` | `Nekrose`, `Fibrinbelag` |
| `Großflächig trockene schwarze Nekrosen (Eschar) an Ferse und lateraler Fußseite; kleinere Areale mit gelblich-fibrinösem Belag proximal; keine erkennbare Granulation.` | `Fibrinbelag`, `Nekrose` |
| `Großflächig, feucht; überwiegend rote Granulation mit gelblichen fibrinösen Belägen/Slough.` | `Fibrinbelag`, `Granulation` |
| `Großflächige schwarz-braune, teils feucht glänzende Nekrose/Schorf ohne sichtbares vitales Gewebe; Übergangszonen mit grauen Belägen.` | `Fibrinbelag`, `Nekrose` |
| `Großflächige schwarz-braune, teils glänzend-feuchte Eschar/Nekrose, fest haftend; randständig gelblich-graue Beläge; kein vitales Granulations- oder Epithelgewebe sichtbar.` | `Fibrinbelag`, `Nekrose` |
| `Großflächige schwarz-braune, trockene, fest haftende Nekrose (Eschar) an der Ferse/lateralem Rückfuß; weitere kleinere nekrotische Läsion am lateralen Vorfuß nahe dem 5. Strahl; kein sichtbares Granulations- oder Epithelgewebe; stellenweise gelblich-fibrinöse Beläge proximal am Knöchel.` | `Fibrinbelag`, `Nekrose` |
| `Großflächige schwarze/braune Nekrosen und gelblich-fibrinöse Beläge, teils feucht; randständig kleine Areale mit frischer Blutung/Granulation.` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Großflächige trockene, schwarze Eschar lateral am Rückfuß/Ferse; kleinere nekrotische Läsion am lateralen Zehenbereich. Umgebung teils stark gerötet, glänzend, keine sichtbare Granulation.` | `Nekrose`, `Rötung` |
| `Großflächige Ulzeration mit überwiegend vitalem, feucht-glänzendem, hell- bis dunkelrotem Granulationsgewebe; eingestreut gelblich-weißliche fibrinöse Beläge (vor allem zentral und distal); keine schwarze Nekrose sichtbar; unregelmäßige Kontur.` | `Fibrinbelag`, `Granulation` |
| `Großflächige, schwarz-braune, trockene Nekrose/Eschar; keine sichtbare Granulation, minimaler erythematöser Saum` | `Nekrose` |
| `Großflächige, trockene schwarze Eschar (nekrotisches Gewebe) am Fersenpolster, keine sichtbare Granulation oder Sickerblutung.` | `Nekrose` |
| `Großflächiger gelblich-bräunlicher fibrinöser Belag mit feuchtem Wundbett; teils rötliche Granulation sichtbar; oberflächlich.` | `Fibrinbelag`, `Granulation` |
| `Großflächiger gelblich-fibrinöser Belag, teils serös‑blutig unterlaufen; oberflächlicher bis teildermaler Substanzverlust.` | `Fibrinbelag` |
| `Großflächiger gelb‑grünlicher Fibrinbelag/Slough mit einzelnen nekrotischen Arealen distal; feucht, kaum sichtbare Granulation.` | `Fibrinbelag`, `Nekrose` |
| `Großflächiger, feucht glänzender Wundgrund mit hell- bis dunkelroter Granulation; multiple gelblich‑weiße Fibrinbeläge/Slough-Inseln; unregelmäßige Oberfläche; keine trockene Nekrose sichtbar.` | `Granulation`, `Fibrinbelag` |
| `Großflächiger, oberflächlicher bis mäßig tiefer Ulkus mit überwiegend vitaler, feucht glänzender, hell- bis dunkelroter Granulation; multiple gelblich‑weiße Fibrinbeläge/Slough-Inseln; unregelmäßige Oberfläche; keine trockene Nekrose sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Großflächiges, feuchtes Wundbett mit dicken gelblich-grünlichen Fibrinbelägen/Slough; stellenweise rötliche Granulationsinseln; keine schwarze Trockennekrose erkennbar.` | `Fibrinbelag`, `Granulation` |
| `grünlich belegt, deutet auf Infektion hin, Nekrosen am  Wundgrund belegt` | `Belag`, `Infektion`, `Nekrose` |
| `Hauptläsion: flaches, ovales Ulkus mit gelblich-beigem fibrinösem Belag, randständig teils rötlich, feucht glänzend; keine schwarze Nekrose, feuchtem Wundbett. Zweite kleinere, oberflächliche Läsion lateral mit rötlichem, keine sichtbaren tieferen Strukturen.` | `Ulzeration`, `Fibrinbelag`, `Rötung` |
| `Hauptläsion: flaches, ovales Ulkus mit gelblich-beigem fibrinösem Belag, randständig teils rötlich, feucht glänzend; keine schwarze Nekrose, keine sichtbaren tieferen Strukturen. Zweite kleinere, oberflächliche Läsion lateral mit rötlichem, feuchtem Wundbett.` | `Fibrinbelag`, `Rötung` |
| `Hämangiome sind Neoplasien ( Neubildungen) , umschriebenes Hämangiom, klare Abgrenzung. segmentale Fehlbildung.
Behandlung unbedingt notwendig.` | `Hämangiom` |
| `hämatös` | `Hämatom` |
| `Irregulärer Ulkus mit gelblichen fibrinösen Belägen und Anteilen rötlicher Granulation; feucht glänzend.` | `Fibrinbelag`, `Granulation` |
| `Kavitäre Ulzeration mit überwiegend gelblich-cremigem fibrinösem Belag/Slough; stellenweise rötliche Granulationsinseln an der Innenwand; feucht mit dickflüssigem Exsudat; keine freiliegenden Knochen oder Sehnen sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Granulation`, `Exsudat` |
| `Kein freiliegender Wundgrund sichtbar; intakte bzw. teils abgehobene Epidermis mit Hämatom und Blasen` | `Blasenbildung`, `Hämatom` |
| `Kleine Nekrose oberhalb des großen offenen Ulcus, muss mit versorgt werden
sonstig massiv belegt, Nekrosenbildung bei Nichtbehandlung wahrscheinlich. Prüfung ob knöcherne Strukturen / Sehnen betroffen sind` | `Nekrose`, `Belag` |
| `Kleine punktförmige Öffnungen/Pusteln mit serösem bis seropurulentem Exsudat, umgebend entzündlich gerötet; kein sichtbarer Nekrosenbelag.` | `Rötung`, `Exsudat` |
| `Kleine runde Öffnung mit gelb-grünlichem purulentem/fibrinösem Belag (Eiterpfropf); kein sichtbares Granulations- oder Epithelgewebe.` | `Fibrinbelag`, `Infektion` |
| `Kleine rundliche Ulzeration mit gelblich-fibrinösem Belag, flach bis mäßig tief; kein sichtbares nekrotisches Gewebe.` | `Ulzeration`, `Fibrinbelag` |
| `Kleine, serös gefüllte Blase mit möglicher punktueller Erosion; kein nekrotisches Gewebe sichtbar.` | `Blasenbildung` |
| `Kleiner ovaler Defekt mit gelblich-fibrinösem Belag, kaum sichtbare Granulation, oberflächlich.` | `Fibrinbelag` |
| `Kleiner runder Ulkus (~1.5–2 cm) mit gelblich-weißen fibrinösen Belägen, punktuell rötlich/blasende Areale; oberflächlich und feucht.` | `Ulzeration`, `Fibrinbelag`, `Rötung`, `Blasenbildung` |
| `kleinere Nekrosen, belegt` | `Nekrose`, `Belag` |
| `Kleines rundes Ulkus mit gelblich-fibrinösem Belag; kein freiliegendes tieferes Gewebe sichtbar.` | `Ulzeration`, `Fibrinbelag` |
| `Kleines rundes Ulkus mit gelblich-fibrinösen Belägen, eher trocken; kein deutlich granulierendes Gewebe sichtbar.` | `Fibrinbelag` |
| `Kleines, ovales Ulkus mit gelblich-fibrinösem Belag; feucht, keine freiliegenden Strukturen sichtbar.` | `Ulzeration`, `Fibrinbelag` |
| `Kraterförmige Ulzeration mit überwiegend gelblich-weißem fibrinösem Belag (Slough) und Anteilen rötlichen, feuchten Granulationsgewebes; kein schwarz nekrotisches Gewebe erkennbar.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Kraterförmiges Ulkus mit gelblichen fibrinösen Belägen, teilweise rötlich-granulierende Areale; mäßig exsudierend.` | `Ulzeration`, `Fibrinbelag`, `Rötung`, `Granulation` |
| `Kräftig rot, homogen granulierend, feucht-glänzend ohne sichtbare Nekrosen oder dicke Fibrinbeläge.` | `Rötung`, `Granulation` |
| `leichte Granulation, belegt mit Fibrin, 2 Inseln Beurteilung hier schwer, da nicht genau zu erkennen sind, ob es ich um Nekrosen handelt.` | `Granulation`, `Fibrinbelag` |
| `Livide bis schwärzliche Areale mit partiell intakten/rupturierten Blasen; oberflächliche Hautnekrosen, kein sichtbares Granulationsgewebe; flächige Beteiligung ohne erkennbare Taschen.` | `Blasenbildung`, `Nekrose` |
| `massive großflächige Verbrennung teilweise 4. Grades, je mehr es vom Wundzentrum nach außen geht werden Verbrennungen 3 7 2. und 1. Grades sichtbar. Nach der 9 er regel könnten hier bis zu 9 % der Körperoberfläche geschädigt sein` | `Verbrennung` |
| `Mehrere flache bis mäßig vertiefte, teilweise konfluierende Ulzera mit ausgedehntem gelb-grünlichem fibrinösem Belag/Slough; stellenweise rötliche, feinkörnige Granulation sichtbar; feucht glänzend; keine schwarze Nekrose.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Mehrere flache Ulzera mit gelblich-fibrinösen Belägen, teils granuliert; einzelne Blutkrusten, kein freiliegender Knochen/Sehne sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Mehrere flache, rundliche Ulzera mit gelblichen Fibrinbelägen, teils rötliche Granulationsinseln; feucht glänzend.` | `Ulzeration`, `Fibrinbelag`, `Rötung`, `Granulation` |
| `Mehrere konfluierende, oberflächlich erodierte Areale mit feucht-glänzend rotem Gewebe; punktuell serös-sanguinöse Anteile; kein nekrotisches Gewebe erkennbar; teils weißliche, schuppige Auflagerungen an und um die Erosionen.` |  |
| `Mehrere oberflächliche Erosionen mit feuchtem, rosig-rotem, glänzendem Wundgrund; teils intakte seröse Blasen, teils rupturierte Blasen mit freiliegender Dermis; keine sichtbaren Nekrosen oder dicker Fibrinbelag.` | `Blasenbildung` |
| `Mehrere oberflächliche Läsionen (Erosionen/Ulzera) mit gelb-beigen Fibrinbelägen und rötlicher Granulation; feucht-glänzend; keine schwarze Nekrose sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Mehrere oberflächliche Ulzerationen mit gelblich-grünlichem fibrinösem Belag, feucht; teils rote Granulationsinseln.` | `Ulzeration`, `Fibrinbelag`, `Granulation`, `Rötung` |
| `Mehrere sakrale Ulzera, teils tiefer liegend; gemischter Wundgrund mit rötlichem Granulationsgewebe und gelblichen Fibrinbelägen; feucht.` | `Ulzeration`, `Granulation`, `Fibrinbelag`, `Rötung`, `Feucht` |
| `mehrere Stadien zu erkennen, nekrotisch, belegt, teilweise granuliert` | `Nekrose`, `Belag`, `Granulation` |
| `Mehrere tiefe Ulzera mit gelblich-weißem Fibrinbelag und schwarzer Nekrose, feucht, teils mit Taschenbildung.` | `Ulzeration`, `Fibrinbelag`, `Nekrose`, `Taschenbildung` |
| `Mehrere tiefe Ulzerationen mit gelblich-fibrinösen Belägen und schwarzer Nekrose, teilweise rötlich-granulierende Areale, feucht.` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Mehrere Ulzera: 1) rundliches Ulkus am Fußrand mit zentraler schwarz‑brauner, trockener Nekrose/Eschar; 2) irreguläres Ulkus plantar am Vorfuß/Zehenbasis mit rötlicher Granulation, gelblich-fibrinösen Belägen und teils blutigen Auflagerungen; insgesamt feucht glänzend, keine sichtbaren Sehnen oder Knochen.` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Mehrere ulzerierende Läsionen, teils mit schwarzer Nekrose/Eschar, teils gelb-fibrinös belegt; randständig teils rötlich, vereinzelt feuchte Areale mit beginnender Granulation.` | `Ulzeration`, `Nekrose`, `Fibrinbelag`, `Rötung`, `Granulation` |
| `Mehrere zirkuläre bis ovale, flache bis mäßig tiefe Ulzera mit gelblich-beigen Fibrinbelägen/Slough; zentral/peripher rötliche Granulationsinseln; feucht glänzend; keine trockene Schwarznekrose sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Mischbild aus vitalem Granulationsgewebe mit gelblich-fibrinösen Belägen; zwei tiefer reichende Ulzera, kein freiliegender Knochen sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Mischuntergrund. Fibrinbelag, nekrotisch, teils mit Granulationsinseln` | `Mischuntergrund`, `Fibrinbelag`, `Nekrose`, `Granulation` |
| `Multiple rund-ovale, teils konfluierende Ulzera mit gelblich-beigem fibrinösem Belag; Abschnitte mit rötlicher Granulation; vereinzelt hämorrhagische Krusten/Schorfinseln; überwiegend oberflächlich bis partiell dermal, feucht-glänzend ohne sichtbare tiefe Strukturen.` | `Fibrinbelag`, `Granulation` |
| `nekrotisch` | `Nekrose` |
| `nekrotisch belegt` | `Nekrose`, `Fibrinbelag` |
| `Nekrotisch und durch Infektion belegt, Wunde bildet Geruch, Frage der Keimbestimmung wichtig, Wundabstrich notwendig,` | `Nekrose`, `Infektion` |
| `nekrotisch und fibrinös belegt` | `Nekrose`, `Fibrinbelag` |
| `nekrotisch, feuchte nekrose` | `Nekrose` |
| `nekrotisch, wandständige Nekrosen` | `Nekrose` |
| `Nekrotische und fibrinös belegte Wunde- auf Grund der Mazeration nach plantar hin könnte mäßige Exsudation auftreten. Wundinfektion möglich` | `Nekrose`, `Fibrinbelag`, `Mazeration` |
| `Oberflächlich bis mäßig tiefes Ulkus mit gelblich-fibrinösen Belägen und Anteilen rötlicher Granulation.` | `Ulzeration`, `Fibrinbelag`, `Rötung`, `Granulation` |
| `Oberflächliche Ulzeration mit gelb-grünlichem Fibrin-/Slough-Belag, stellenweise rötliche Granulation sichtbar; feucht, unregelmäßige Kontur, glänzende Oberfläche.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `oberflächliche Ulzeration mit gelblich-weißen Fibrinbelägen und vereinzelten rötlich-granulierenden Arealen; keine trockene Nekrose sichtbar` | `Fibrinbelag`, `Granulation` |
| `Oberflächliche Ulzerationen mit gelblichen Fibrinbelägen und Anteilen von feuchtem rotem Granulationsgewebe; keine schwarze Nekrose sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Rötung`, `Granulation` |
| `Oberflächliche, feuchte, rötliche Dermis mit erosiven Arealen; multiple intakte und rupturierte seröse Blasen; kein nekrotisches Gewebe sichtbar.` | `Rötung`, `Blasenbildung` |
| `Oberflächliche, teils nässende Erosionen mit gerötetem Wundgrund; keine tiefe Nekrose sichtbar.` | `Rötung` |
| `Oberflächlicher, größerer Defekt mit gelblich-fibrinösen Belägen und teils rötlicher Granulation; feucht glänzend, kein schwarzes Nekrosegewebe sichtbar.` | `Fibrinbelag`, `Rötung`, `Granulation` |
| `Oberflächlicher, irregulär geformter Wundgrund mit überwiegend gelblich-grünlichem fibrinösem Belag/Slough; dazwischen rötliche, feucht-glänzende Granulation; kein trockener Nekroseanteil; flach ohne sichtbare Taschen.` | `Fibrinbelag`, `Granulation` |
| `Oberflächliches Ulkus mit ausgedehnten gelblichen Fibrinbelägen, teils rötlich granulierend; feucht glänzend.` | `Ulzeration`, `Fibrinbelag`, `Rötung`, `Granulation` |
| `Oberflächliches Ulkus mit gelb-grünlichem Fibrin-/Belag, teils nekrotisch; feucht, unregelmäßiger Wundgrund.` | `Ulzeration`, `Fibrinbelag`, `Nekrose` |
| `Oberflächliches Ulkus mit gelblich-fibrinösen Belägen, randständig teils granulierend; kleine zweite Läsion lateral.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Oberflächliches Ulkus mit gelblich-fibrinösen Belägen; randständig teils epithelisierend; zweite kleine oberflächliche Läsion lateral.` | `Fibrinbelag`, `Wundrandepithelisierung` |
| `Oberflächliches, ovales Ulkus mit überwiegend gelblich-weißlichem, feuchtem Fibrinbelag; stellenweise rötliche Granulation sichtbar; keine schwarze Nekrose; unregelmäßige Kontur, glänzende Oberfläche.` | `Fibrinbelag`, `Granulation` |
| `offenen stelle entzündet. belegt, nekrotisch, geschlossene stelle nekrotisch` | `Entzündung`, `Belag`, `Nekrose` |
| `Ovale, flache Ulzeration mit überwiegend gelblich-fibrinösem Belag (ca. 70-80%) und dazwischen rötlicher, feucht glänzender Granulation (ca. 20-30%); keine schwarze Nekrose, keine sichtbare Sehnen- oder Knochenexposition.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Ovale, flache Ulzeration mit überwiegend gelblich-fibrinösem Belag (ca. 70–80%) und dazwischen rötlicher, feucht glänzender Granulation (ca. 20–30%); keine schwarze Nekrose, keine sichtbare Sehnen- oder Knochenexposition.` | `Fibrinbelag`, `Granulation` |
| `Ovale, mäßig tiefe Ulzeration mit überwiegend rötlichem, feuchtem Granulationsgewebe; randständig teils adhärente gelblich-fibrinöse Beläge; keine schwarze Nekrose sichtbar.` | `Ulzeration`, `Granulation`, `Fibrinbelag` |
| `Ovaler Defekt mit zentralem gelblich-beigem Fibrin/Slough, peripher rötliches granulierendes Gewebe; feucht-glänzende Oberfläche; keine sichtbare trockene Nekrose oder freiliegende tiefe Strukturen.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Ovales Ulkus mit dicken gelb-weißlichen Fibrinbelägen, zentral teils grau-schwarze nekrotische Areale; kaum sichtbare Granulation.` | `Ulzeration`, `Fibrinbelag`, `Nekrose` |
| `Ovales Ulkus mit gelblich-fibrinösem Belag, feucht-glänzend; punktuell gerötete Granulation sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Ovales Ulkus mit randständigem gelblich-fibrinösem Belag und zentralen Granulationsarealen; keine freiliegenden Strukturen sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Ovales Ulkus, zentral überwiegend gelblich-bräunlicher Fibrinbelag/Slough (~60–70%), peripher rötliche feucht wirkende Granulation (~30–40%); keine freiliegenden Sehnen oder Knochen erkennbar; moderat tief, klar begrenzte Defektzone.` | `Fibrinbelag`, `Granulation` |
| `Ovales, oberflächliches Ulkus mit gelblich-fibrinösem Belag zentral, peripher rötlich granulierend.` | `Fibrinbelag`, `Granulation` |
| `Punktförmige Läsion mit gelb-grünlichem Belag/Eiterpfropf, Tiefe unklar.` | `Fibrinbelag` |
| `Punktförmige, schlitzartige Fistelöffnung(en); Wundgrund nicht einsehbar. Eine Öffnung mit klar-gelblich seröser Flüssigkeit; kein sichtbarer Fibrin- oder Nekrosebelag.` | `Ulzeration`, `Exsudat` |
| `Runde Ulzeration mit zentral gelblich-fibrinösem Belag, mäßig feucht; peripher schmaler erythematöser Saum, kein freiliegender Knochen/Sehne sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Rötung` |
| `Runde, oberflächliche Läsion mit gelblich-fibrinösem Belag und punktuellen Granulationen; feucht glänzend.` | `Fibrinbelag`, `Granulation` |
| `Runder, kraterförmiger Defekt mit überwiegend gelblich-fibrinösem Belag; feucht glänzend; keine schwarze Nekrose sichtbar; kaum bis keine erkennbare Granulation.` | `Ulzeration`, `Fibrinbelag` |
| `Rundliche Ulzeration mit überwiegend gelblich-fibrinösem Belag; punktuell rote, feuchte Areale/Granulationsinseln; glänzend-feucht, keine schwarze Nekrose sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Granulation` |
| `Rötlich-feuchtes, gut durchblutetes Granulationsgewebe, punktuell dünner Fibrinbelag; keine Nekrosen sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Rötliches, feuchtes Granulationsgewebe; teils gelblich fibrinöser Belag randständig; kraterförmiger, tiefer Defekt ohne schwarze Nekrosen; glänzende Oberfläche.` | `Fibrinbelag`, `Granulation` |
| `Sauber, bis auf die aufgetragene Salbe` | `Sauber` |
| `sauberer Wundgrund mit Inseln von Granulation` | `Sauber`, `Granulation` |
| `Sauberer Wundgrund mit kleinen Fibrininseln` | `Sauber`, `Fibrinbelag` |
| `Schwarz-braune Nekrosen und fest anhaftende Fibrinbeläge; teils blutiges, freiliegendes Gewebe am Vorfuß; mehrere oberflächliche bis mäßig tiefe Ulzera.` | `Fibrinbelag`, `Nekrose` |
| `Schwarze Nekrosenanteile mit dicken gelb-grünlichen fibrinösen Belägen, feucht; peripher teils gerötetes/angegriffenes Gewebe.` | `Nekrose`, `Fibrinbelag`, `Rötung` |
| `sehr ausgeprägte massive Nekrose, teilweise frei liegende Strukturen, blutig seröses Exsudat` | `Nekrose`, `Freiliegende Strukturen`, `Exsudat` |
| `stark belegt, neben Fibrin könnte es sich auch um feuchte, wandständige Nekrosen handeln` | `Fibrinbelag` |
| `stark belegte, super infizierte Wunde, teilweise freiliegende Strukturen,
Nekrosen.` | `Belag`, `Infektion`, `Freiliegende Strukturen`, `Nekrose` |
| `stark belgtes Ulcus, teilweise einzelne Granulationsinseln,` | `Belag`, `Granulation` |
| `stark geschädigt, nekrotisch, fibrinös belegt, freiliegende Sehnen / Knochen` | `Nekrose`, `Fibrinbelag`, `Freiliegende Sehnen`, `Freiliegende Knochen` |
| `stark infiziert, massiv belegt` | `Infektion`, `Belag` |
| `Stark nässend; dicke gelb-grünliche Fibrin-/Beläge mit mutmaßlichem Biofilm, teils nekrotische Areale; kaum Granulation sichtbar.` | `Fibrinbelag`, `Biofilm`, `Nekrose` |
| `starke Granulation, überschießendes Gewebe, infektfrei` | `Granulation`, `Hypergranulation` |
| `teilweise fibrinbelegt mit einzelnen Granulationsinseln` | `Fibrinbelag`, `Granulation` |
| `Teilweise freiliegende, feucht-rosige Dermis mit oberflächlichen Erosionen; mehrere intakte und rupturierte seröse Blasen, vereinzelte dünne Fibrinauflagen.` | `Blasenbildung`, `Fibrinbelag` |
| `teilweise nekrotisch, belegt` | `Nekrose`, `Belag` |
| `Tief klaffende, längsovale Wunde; Wundgrund überwiegend mit dicken gelb-beigen fibrinösen Belägen/Slough bedeckt, teils graugelb; feucht-glänzend; kaum/kein sichtbares Granulationsgewebe; unregelmäßige Taschen/Kavernen erkennbar.` | `Fibrinbelag`, `Taschenbildung` |
| `Tiefe moderat, kavitäre Ulzeration mit überwiegend gelblich-cremigem fibrinösem Belag/Slough; stellenweise rötliche Granulationsinseln an der Innenwand; feucht mit dickflüssigem Exsudat; keine freiliegenden Knochen oder Sehnen sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Granulation`, `Exsudat` |
| `Tiefe moderat, Wundbett nahezu vollständig (ca. 90-100%) mit gelb-beigem, faserigem Fibrin/Slough bedeckt; kein schwarzer Schorf sichtbar; kaum bis keine Granulation erkennbar; vereinzelte rötliche Areale am Boden; Wunde klar begrenzt, feucht-glänzendem, keine offen erkennbaren freiliegenden tieferen Strukturen.` | `Fibrinbelag`, `Rötung` |
| `Tiefe, kavitäre Ulzeration mit überwiegend gelblich-cremigem fibrinösem Belag/Slough; stellenweise rötliche Granulationsinseln an der Innenwand; feucht mit dickflüssigem Exsudat; keine freiliegenden Knochen oder Sehnen sichtbar.` | `Exsudat`, `Fibrinbelag`, `Granulation` |
| `Tiefe, kraterförmige Ulzeration mit überwiegend gelblich-weißem fibrinösem Belag (Slough) und Anteilen rötlichen, feuchten Granulationsgewebes; kein schwarz nekrotisches Gewebe erkennbar.` | `Fibrinbelag`, `Granulation` |
| `Tiefer Defekt mit dicken gelblichen Fibrin-/Schleimbelägen, teils nekrotisch; kaum Granulation sichtbar.` | `Fibrinbelag`, `Nekrose` |
| `Tiefer Defekt mit überwiegend vitalem, feuchtem Granulationsgewebe; randständig gelblich-fibrinöse Beläge.` | `Granulation`, `Fibrinbelag` |
| `tiefer Dekubitus Wundgrund belegt, Taschenbildung teilweise nekrotisch` | `Belag`, `Taschenbildung`, `Nekrose` |
| `Tiefer Ulkus mit gelblich-fibrinösen Belägen, teils nekrotisch, wenig Granulation; Höhle mit möglicher Randunterminierung.` | `Fibrinbelag`, `Granulation`, `Nekrose`, `Taschenbildung` |
| `Tiefere Wunde mit dicken gelblichen fibrinösen Belägen/Detritus, kaum sichtbare Granulation; möglicherweise Wundtaschen.` | `Fibrinbelag`, `Granulation`, `Taschenbildung` |
| `Tieferes Ulkus mit dicken gelb-gräulichen Fibrinbelägen, feucht; kaum sichtbares Granulationsgewebe.` | `Ulzeration`, `Fibrinbelag` |
| `Tiefes Ulkus mit gelb- bis grünlichem Fibrin-/Belag, teils avital, Biofilm-verdächtig; Höhle mit möglicher Unterminierung; geringe Inseln von Granulation.` | `Ulzeration`, `Fibrinbelag`, `Biofilm`, `Unterminierung`, `Granulation` |
| `Tiefes, kavernöses Areal mit überwiegend gelb-braunem, dickem fibrinös-purulentem Belag; vereinzelte nekrotische Areale; kaum sichtbares vitales Granulationsgewebe; feucht glänzend.` | `Fibrinbelag`, `Nekrose`, `Taschenbildung` |
| `Tiefes, rundes Ulkus mit zentral gelb-weißem Fibrin/nekrotischen Anteilen; feuchte Beläge, mehere Läsionen sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Nekrose` |
| `Tiefes, rundes Ulkus mit zentral gelb-weißem Fibrin/nekrotischen Anteilen; feuchte Beläge, mehrere Läsionen sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Nekrose` |
| `Ulzeration mit gelblich-fibrinösem Belag am Rand, zentral teils vitales rötliches Granulationsgewebe; mäßig tiefe Kavität, keine trockene Nekrose sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Rötung`, `Granulation` |
| `Unregelmäßig konfiguriertes, eher flaches Ulkus mit überwiegend gelblich-weißlichen fibrinösen Belägen und zähem Exsudat; dazwischen rötliche, feucht-körnige Granulation; keine schwarze Nekrose sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Granulation`, `Exsudat` |
| `verbrannte  Epidermis` | `Verbrennung` |
| `Verbrennungen, Blasenbildung, offene Wunden keine verbrannten Sehnen / Knochen  epidermis geschädigt` | `Verbrennung`, `Blasenbildung` |
| `Vitales, homogen granulierendes Gewebe, feucht glänzend, keine sichtbaren Beläge oder Nekrosen.` | `Granulation` |
| `vitalrotes, glänzend-feuchtes Granulationsgewebe, teils bereits beginnende Epithelisierung, keine Nekrosen sichtbar` | `Granulation`, `Wundrandepithelisierung` |
| `wandständige Nekrose, Prüfung, ob Knochen / Sehnen betroffen sind. Unbedingt chirurgisch intervenieren.
Druckentlastung essentiell.` | `Nekrose` |
| `Weitgehend rötlich-granulierend mit teils fibrinösen Belägen; feucht glänzend, mehere oberflächliche Läsionen im Cluster.` | `Rötung`, `Granulation`, `Fibrinbelag` |
| `Weitgehend rötlich-granulierend mit teils fibrinösen Belägen; feucht glänzend, mehrere oberflächliche Läsionen im Cluster.` | `Rötung`, `Granulation`, `Fibrinbelag` |
| `Weitläufige, flache Ulzeration mit gelblich-fibrinösem Belag, feucht; vereinzelte punktförmige Blutungen; keine freiliegenden Strukturen erkennbar.` | `Fibrinbelag` |
| `Wundbett nahezu vollständig (ca. 90-100%) mit gelb-beigem, feucht-glänzendem, faserigem Fibrin/Slough bedeckt; kein schwarzer Schorf sichtbar; kaum bis keine Granulation erkennbar; vereinzelte rötliche Areale am Boden; Wunde klar begrenzt, Tiefe moderat, keine offen erkennbaren freiliegenden tieferen Strukturen.` | `Fibrinbelag` |
| `Wundbett vollständig von trockener, schwarz-brauner, fest anhaftender Ledernekrose (Eschar) bedeckt; teils grauweißliche Anteile; keine sichtbare Granulation oder Epithelisierung.` | `Nekrose` |
| `Zentral gelblich-fibrinöser Belag, flach; geringe/keine sichtbare Granulation; kein nekrotisches Gewebe erkennbar.` | `Fibrinbelag` |
| `Zentral gelblich-weisslicher Fibrinbelag mit zwei rötlichen Granulationsinseln; oberflächlich, feucht.` | `Fibrinbelag`, `Granulation` |
| `Zentral gelblicher fibrinöser Belag, randständig teils rötliche Granulation; kein freiliegender Knochen sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Zentral schwarz-braune Eschar mit fest anhaftenden Belägen; randständig livid-erythematös und leicht erhaben.` | `Nekrose`, `Rötung` |
| `Zentral schwarz-braune Nekrose, umgebend gelblich-fibrinöser Belag mit feuchtem Exsudatfilm; kein vitales Granulationsgewebe erkennbar.` | `Nekrose`, `Fibrinbelag` |
| `Zentral trockene schwarz‑braune Nekrose (Eschar) mit gelblich‑bräunlichem Fibrin/Schorf; kein sichtbares Granulations- oder Epithelgewebe.` | `Nekrose`, `Fibrinbelag` |
| `Zentral überwiegend gelblich-weißlicher fibrinöser Belag (Slough), feucht; randständig schmaler rötlicher Saum mit beginnender Granulation; keine schwarze Nekrose sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Zentrale schwarz-braune Eschar mit gelblich-fibrinösen Arealen; verhärteter, livid-erythematöser Rand.` | `Fibrinbelag`, `Nekrose`, `Rötung` |
| `Zentrale schwarz-gelbe Eschar mit fest anhaftenden Belägen; randständig livid-erythematös und leicht erhaben.` | `Nekrose` |
| `Zwei benachbarte Ulzera: proximal überwiegend gelb-beiger fibrinöser Belag; distal rötlich-feuchtes, teils granuliertes Gewebe. Keine schwarze Nekrose sichtbar. Oberflächlich bis mäßig tief.` | `Fibrinbelag`, `Granulation` |
| `Zwei getrennte Ulzera. Proximal: ovaler Defekt mit überwiegend gelb-grauem Fibrin/Slough (ca. 60-70%), restlich rötlich-feuchtes Gewebe. Distal: gemischter Wundgrund mit randständiger rötlicher Granulation und zentral schwarz-brauner trockener Nekrose/Schorf; teils serös-blutige Beläge. Tiefe bis ins subkutane Gewebe, keine freiliegenden Sehnen oder Knochen sichtbar.` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Zwei größere kraterförmige Ulzera mit überwiegend vitaler roter Granulation und teils gelblich-beigen fibrinösen Belägen; feuchtes, glänzendes Wundbett; keine trockene Schwarznekrose sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Zwei Läsionen: kaudal ausgedehnte schwarze Nekrose (Eschar), kranial gelb-grünlicher fibrinöser Belag; feuchtes Milieu, kein sichtbares Granulationsgewebe.` | `Nekrose`, `Fibrinbelag` |
| `Zwei oberflächliche Ulzerationen mit gelblichen fibrinösen Belägen, teils rötlich granulierend, feucht; keine ausgedehnte trockene Nekrose sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Rötung`, `Granulation` |
| `Zwei tiefe Ulzerationen mit dickem gelblich-weißlichem fibrinösem/purulentem Belag; randständig teils rötliche Granulation; feucht, kein schwarzes Nekrosengewebe sichtbar.` | `Fibrinbelag`, `Granulation`, `Infektion` |
| `Zwei Ulzera mit gelb-grünlichen Fibrinbelägen und teils schwarzer Nekrose; feuchter Wundgrund mit randständiger Rötung.` | `Ulzeration`, `Fibrinbelag`, `Nekrose`, `Rötung` |
| `Zwei Ulzera: oberes Ulkus mit dickem gelblich-grünlichem Fibrin-/Schmierbelag, feucht glänzend; unteres, größeres Ulkus mit ausgedehnter schwarzer, teils feucht glänzender Nekrose/Eschare. Kein sichtbar vitales Granulations- oder Epithelgewebe; Beläge überwiegend adhärent.` | `Ulzeration`, `Fibrinbelag`, `Nekrose` |
| `Zwei ulzerierende Läsionen mit dickem gelb-weißlichem Fibrinbelag/Detritus und viskösem Exsudat; kein freiliegender Knochen oder Sehne sichtbar.` | `Ulzeration`, `Fibrinbelag`, `Exsudat` |
| `Überwiegend dicke gelb-grüne, schmierig-fibrinöse Beläge mit purulentem, viskösem Exsudat; dazwischen rötliche Granulationsinseln; einzelne bräunlich-dunklere Areale; Wundbett feucht und unregelmäßig, keine freiliegenden Sehnen oder Knochen sichtbar.` | `Exsudat`, `Fibrinbelag`, `Granulation`, `Infektion` |
| `Überwiegend feucht-rote Granulation, flach; zwei zentral gelegene rundliche weißlich-gelbliche Fibrininseln/Beläge; keine schwarze Nekrose; beginnende Epithelisierung vom Rand.` | `Fibrinbelag`, `Granulation`, `Wundrandepithelisierung` |
| `Überwiegend gelb-grauer fibrinöser Slough/Belag, feucht und zäh; kaum sichtbares Granulationsgewebe; unregelmäßig-oval.` | `Fibrinbelag` |
| `Überwiegend gelb-grauer, dicker fibrinöser/slough-Belag mit teils nekrotischem Aspekt; feucht, zäh; kaum bis kein vitales Granulationsgewebe sichtbar; Anzeichen von Tiefe/Unterminierung.` | `Fibrinbelag`, `Nekrose`, `Taschenbildung` |
| `Überwiegend gelb-grünlicher fibrinöser Belag; zentral schwarz-brauner Nekroseanteil (Eschar); feuchte, glänzende Oberfläche; keine sichtbare Granulation oder Epithelinseln.` | `Fibrinbelag`, `Nekrose` |
| `Überwiegend gelb-weißlicher Fibrin-/Slough-Belag mit einzelnen Arealen rötlicher Granulation; feucht-glänzende Oberfläche; keine schwarze Nekrose sichtbar; keine freiliegenden tieferen Strukturen erkennbar.` | `Fibrinbelag`, `Granulation` |
| `Überwiegend gelb-weißlicher Fibrin-/Slough-Belag mit einzelnen grau-schwarzen nekrotischen Arealen; randständig geringe rötliche Gewebeanteile; unregelmäßiger, teilweise kavitiert; feucht glänzend; keine exponierten Knochen/Sehnen sichtbar.` | `Fibrinbelag`, `Nekrose`, `Rötung`, `Taschenbildung` |
| `Überwiegend gelb-weißlicher fibrinöser Belag (Slough), stellenweise rötliche Granulation sichtbar; feucht, unregelmäßig-kraterförmig; keine trockene schwarze Nekrose erkennbar.` | `Fibrinbelag`, `Granulation` |
| `Überwiegend gelblich-beiger Fibrinbelag/Slough (~70%) mit randständiger rötlicher, feucht-glänzender Granulation; keine schwarze Nekrose sichtbar; vereinzelte punktförmige Blutungen.` | `Fibrinbelag`, `Rötung`, `Granulation` |
| `Überwiegend gelblich-beiger Fibrinbelag/Slough (~70%) mit randständiger rötlicher, feuchter Granulation (~30%); kein schwarzes Nekrosegewebe sichtbar; Wundbett feucht-glänzend, mäßige Tiefe; keine freiliegenden Strukturen (Knochen/Sehne) erkennbar.` | `Fibrinbelag`, `Granulation` |
| `Überwiegend gelblich-beiger fibrinöser Belag mit Anteilen rötlicher, feucht-glänzender Granulation; keine schwarze Nekrose sichtbar; vereinzelte punktförmige Blutungen.` | `Fibrinbelag`, `Rötung`, `Granulation` |
| `Überwiegend gelblich-beiger, dicker Fibrin-/Belag mit teils grünlicher Tönung, feucht-glänzend; randständig vereinzelte rötliche granulierende Areale und punktförmige Blutungen; keine schwarze Nekrose sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Überwiegend gelblich-beiger, feucht-glänzender Fibrin-/Slough-Belag; ausgedehnte dunkelbraun-schwarze Nekrose-/Escharareale; vereinzelte rötliche Granulationsinseln, vor allem randständig; heterogene Tiefenwirkung` | `Fibrinbelag`, `Granulation`, `Nekrose` |
| `Überwiegend gelblich-weißer Fibrinbelag/Biofilm, dazwischen kleine Inseln granulierenden, roten Gewebes; feucht glänzend.` | `Fibrinbelag`, `Biofilm`, `Granulation`, `Rötung` |
| `Überwiegend gelblich-weißer Fibrinbelag/Slough mit einzelnen rötlichen Granulationsinseln; feucht-glänzend; oberflächlich bis mitteltief; kein trockener schwarzer Nekroseschorf; keine freiliegenden Sehnen oder Knochen sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Überwiegend gelblich-weißlicher Fibrin-/Slough-Belag mit einzelnen grau-schwarzen nekrotischen Arealen; randständig geringe rötliche Gewebeanteile; unregelmäßiger, mäßig tiefer Defekt.` | `Fibrinbelag`, `Nekrose` |
| `Überwiegend gelblich-weißlicher fibrinöser Belag mit Anteilen rötlicher Granulation; kein freiliegender Knochen sichtbar.` | `Fibrinbelag`, `Rötung`, `Granulation` |
| `Überwiegend granulierendes, rötlich bis dunkelrotes, feuchtes Gewebe; mehrere flache, teils konfluierende Ulzera; stellenweise dünner gelblicher Fibrinbelag an den Rändern; keine schwarze Nekrose sichtbar.` | `Fibrinbelag`, `Granulation` |
| `Überwiegend rot-granulierend mit wenigen gelblich-fibrinösen Inseln; feucht; flach.` | `Fibrinbelag`, `Granulation` |
| `Überwiegend rötlich granulierendes Gewebe mit ausgedehnten gelblich-cremigen Fibrinbelägen/Slough; vereinzelt dunklere (bräunlich-schwarze) Beläge distal; feucht glänzend; keine freiliegenden Sehnen oder Knochen erkennbar.` | `Fibrinbelag`, `Nekrose`, `Rötung`, `Granulation` |
| `Überwiegend rötliches, feuchtes Granulationsgewebe mit anteilig gelblich-fibrinösen Belägen; unregelmäßige Ulkusränder; teils kavernös wirkend mit Unterminierung; keine schwarze Nekrose sichtbar.` | `Fibrinbelag`, `Granulation`, `Taschenbildung` |
| `Überwiegend vitales, feuchtes Granulationsgewebe mit geringen fibrinösen Belägen.` | `Granulation`, `Fibrinbelag` |


### 2.PRODUKT_GT_MAPPING

**Anzahl Einträge:** 95

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Actico UlcerSys System` | `Actico UlcerSys System` |
| `ActiFast` | `ActiFast` |
| `ActiFast Schlauchverband` | `ActiFast` |
| `Curafix H` | `Curafix H` |
| `Curapor` | `Curapor` |
| `Curapor transparent` | `Curapor transparent` |
| `Fixierbinde` | `Fixierbinde` |
| `Fixierbinden` | `Fixierbinde` |
| `Haftelast latexfrei` | `Haftelast latexfrei` |
| `Haftelast latexfrei (kohäsive Fixierbinde)` | `Haftelast latexfrei` |
| `Lomatuell H` | `Lomatuell H` |
| `Lomatuell Pro` | `Lomatuell Pro` |
| `Metalline Kompresse` | `Metalline Kompresse` |
| `Mollelast` | `Mollelast` |
| `Mollelast (Elastische Fixierbinde)` | `Mollelast` |
| `Mollelast haft latexfrei` | `Mollelast haft latexfrei` |
| `Porofix` | `Porofix` |
| `ReadyWrap Untere Extremität` | `ReadyWrap Untere Extremität` |
| `Rosidal soft` | `Rosidal soft` |
| `Rosidal TCS` | `Rosidal TCS` |
| `Silkafix` | `Silkafix` |
| `Solvaline N` | `Solvaline N` |
| `Suprasorb A + Ag` | `Suprasorb A + Ag` |
| `Suprasorb A + Ag (Kompresse)` | `Suprasorb A + Ag` |
| `Suprasorb A + Ag Kompresse` | `Suprasorb A + Ag` |
| `Suprasorb A + Ag Tamponade` | `Suprasorb A + Ag` |
| `Suprasorb A Pro` | `Suprasorb A Pro` |
| `Suprasorb A Pro (Kompresse)` | `Suprasorb A Pro` |
| `Suprasorb A Pro (Tamponade)` | `Suprasorb A Pro` |
| `Suprasorb A Pro Kompresse` | `Suprasorb A Pro` |
| `Suprasorb A Pro Tamponade` | `Suprasorb A Pro` |
| `Suprasorb F` | `Suprasorb F` |
| `Suprasorb F Protect` | `Suprasorb F Protect` |
| `Suprasorb G Gel-Kompresse` | `Suprasorb G Gel-Kompresse` |
| `Suprasorb H` | `Suprasorb H` |
| `Suprasorb Liquacel Pro` | `Suprasorb Liquacel Pro` |
| `Suprasorb Liquacel Pro (Kompresse)` | `Suprasorb Liquacel Pro` |
| `Suprasorb Liquacel Pro (Tamponade)` | `Suprasorb Liquacel Pro` |
| `Suprasorb Liquacel Pro Kompresse` | `Suprasorb Liquacel Pro` |
| `Suprasorb Liquacel Pro Tamponade` | `Suprasorb Liquacel Pro` |
| `Suprasorb P` | `Suprasorb P` |
| `Suprasorb P (Heel)` | `Suprasorb P` |
| `Suprasorb P (nicht klebend)` | `Suprasorb P` |
| `Suprasorb P (selbstklebend)` | `Suprasorb P` |
| `Suprasorb P (self-adhesive, sacrum)` | `Suprasorb P` |
| `Suprasorb P + PHMB` | `Suprasorb P + PHMB` |
| `Suprasorb P heel (selbstklebend)` | `Suprasorb P` |
| `Suprasorb P nicht klebend` | `Suprasorb P` |
| `Suprasorb P selbstklebend` | `Suprasorb P` |
| `Suprasorb P Sensiflex` | `Suprasorb P Sensiflex` |
| `Suprasorb P SensiFlex (border rechteckig)` | `Suprasorb P Sensiflex` |
| `Suprasorb P SensiFlex border` | `Suprasorb P Sensiflex` |
| `Suprasorb P SensiFlex border rechteckig` | `Suprasorb P Sensiflex` |
| `Suprasorb P SensiFlex multisite border` | `Suprasorb P Sensiflex` |
| `Suprasorb P SensiFlex multisite border lite` | `Suprasorb P Sensiflex` |
| `Suprasorb P sensitive` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive (finger/toe)` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive (heel)` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive (Heel, selbstklebend)` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive (nicht klebend)` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive (sacrum)` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive (selbstklebend)` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive (selbstklebend) als abdeckender Verband` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive (selbstklebend, sacrum)` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive heel` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive heel (selbstklebend) – als polsternde, absorbierende Sekundärlage über der Tamponade` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive sacrum` | `Suprasorb P Sensitive` |
| `Suprasorb P sensitive selbstklebend` | `Suprasorb P Sensitive` |
| `Suprasorb X` | `Suprasorb X` |
| `Suprasorb X + PHMB` | `Suprasorb X + PHMB` |
| `Suprasorb X + PHMB (Kompresse)` | `Suprasorb X + PHMB` |
| `Suprasorb X + PHMB Kompresse` | `Suprasorb X + PHMB` |
| `Suprasorb X + PHMB Tamponade` | `Suprasorb X + PHMB` |
| `Suprasorb X Kompresse` | `Suprasorb X` |
| `Suprasorb X Pro` | `Suprasorb X Pro` |
| `Suprasorb X Pro (Kompresse)` | `Suprasorb X Pro` |
| `Suprasorb X Pro Kompresse` | `Suprasorb X Pro` |
| `tg Fertigverbände` | `tg Fertigverbände` |
| `tg Fertigverbände (Hand-/Fußverband)` | `tg Fertigverbände` |
| `tg Fertigverbände Hand-/Fußverband` | `tg Fertigverbände` |
| `tg Schlauchverband` | `tg Schlauchverband` |
| `Universalbinde` | `Universalbinde` |
| `Universalbinden` | `Universalbinde` |
| `Vliwaktiv Ag` | `Vliwaktiv Ag` |
| `Vliwaktiv Ag Saugkompresse` | `Vliwaktiv Ag` |
| `Vliwaktiv Ag Tamponade` | `Vliwaktiv Ag` |
| `Vliwasorb Pro` | `Vliwasorb Pro` |
| `Vliwasorb sensitive` | `Vliwasorb sensitive` |
| `Vliwasorb sensitive border` | `Vliwasorb sensitive border` |
| `Vliwasorb sensitive border (sacrum)` | `Vliwasorb sensitive border` |
| `Vliwasorb sensitive border sacrum` | `Vliwasorb sensitive border` |
| `Vliwazell` | `Vliwazell` |
| `Vliwazell Pro` | `Vliwazell Pro` |
| `Vliwazell Pro als abdeckender Verband` | `Vliwazell Pro` |
| `Vliwazell Pro – als hochabsorbierende Sekundärlage über der Tamponade` | `Vliwazell Pro` |


### 2.DEBRIDEMENT_GT_MAPPING

**Anzahl Einträge:** 6

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Autolytisches Debridement` | `Autolytisches Debridement` |
| `Chirurgisches Debridement` | `Chirurgisches Debridement` |
| `Debrisoft Duo` | `Debrisoft Duo` |
| `Debrisoft Lolly` | `Debrisoft Lolly` |
| `Debrisoft Pad` | `Debrisoft Pad` |
| `Ultraschall-assistiertes Debridement (UAW)` | `Ultraschall-assistiertes Debridement (UAW)` |


### 2.WUNDTYP_GT_MAPPING

**Anzahl Einträge:** 143

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `["ausgedehnte, tiefe, nekrotische Ulzeration"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["ausgedehntes, tiefes chronisches Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["ausgeprägtes infiziertes Ulcus cruris","Ulcus cruris venosum"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["chronische Fußwunde / Ulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["chronisches Ulkus cruris"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["chronisches Ulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Dekubitus","Diabetisches Fußulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Dekubitus","Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Dekubitus"]` | `Dekubitus` |
| `["Diabetisches Fußulkus","hochgradig destruierende Fußwunde"]` | `Diabetisches Fußsyndrom (DFS)` |
| `["Diabetisches Fußulkus","ischämisches Ulkus"]` | `Diabetisches Fußsyndrom (DFS)` |
| `["Diabetisches Fußulkus","mit deutlichen Zeichen einer lokalen Infektion und chronisch entzündlicher Hautveränderungen"]` | `Diabetisches Fußsyndrom (DFS)` |
| `["Diabetisches Fußulkus"]` | `Diabetisches Fußsyndrom (DFS)` |
| `["Extravasationsverletzung"]` | `Extravasationsverletzung` |
| `["Gravitationsulzera/Druckulzera"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["großflächiges, flaches chronisches Ulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["kleines, oberflächliches Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["multiple infizierte chronische Fußulzera"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["multiple kleine Ulzera"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["nekrotische Fersenwunde","Dekubitus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["nekrotische ischämische Fußwunde / Gangrän"]` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `["neuroischämisches bzw. arterielles Fußulkus"]` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `["Postoperative Wunde"]` | `Postoperative Wunde / Dehiszenz` |
| `["rundlich-ovales Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["tiefer reichende Ulzerationen am Unterschenkel mit chronisch entzündlicher Umgebung"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Traumatische Wunde","durch Insektenstich"]` | `Traumatische Wunde` |
| `["Ulcus cruris venosum","Adipositas-assoziiert"]` | `Ulcus cruris venosum` |
| `["Ulcus cruris venosum","venös-lymphatischem Ulcus"]` | `Ulcus cruris venosum` |
| `["Ulcus cruris venosum"]` | `Ulcus cruris venosum` |
| `["Ulcus Fußrücken mit deutlicher Gewebedestruktion und freiliegender Sehnenstruktur"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Ulcus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Ulkus cruris"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Ulkus"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["ulzeriertes infantiles Hämangiom mit zentraler Nekrose"]` | `ulzeriertes infantiles Hämangiom mit zentraler Nekrose` |
| `["vaskulitischen Ulzera","möglicher kutaner Vaskulitis"]` | `Ulkus (Ätiologie unspezifisch)` |
| `["Verbrennungswunde"]` | `Verbrennungswunde` |
| `arterielles Ulcus` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `Ausgedehnte feuchte Nekrose` | `Ausgedehnte feuchte Nekrose` |
| `Ausgetrtenes Blut oder Lymphe aus den entsprechenden Gefäßen mit Verteilung an der betroffenen Extremität` | `Ulkus (Ätiologie unspezifisch)` |
| `belegter Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Dekubitus` | `Dekubitus` |
| `Dekubitus an der Ferse` | `Dekubitus` |
| `Dekubitus epuap Stadium 3 / 4` | `Dekubitus` |
| `Dekubitus Grad 2 oder 3 nach EPUAP.
Nicht genau zu definieren, ob sich Unterminierungen vorhanden sind.` | `Dekubitus` |
| `Dekubitus mit Nekrose` | `Dekubitus` |
| `Dekubitus mit Taschenbildung` | `Dekubitus` |
| `Dekubitus sacralbereich` | `Dekubitus` |
| `Dekubitus, vermutlich am Außenknöchel` | `Dekubitus` |
| `Dekubtis im Sakralbereich, großflächig` | `Dekubitus` |
| `diffuse fibrinbelegte und teils infizierte Ulzera am rechten Fuß` | `Ulkus (Ätiologie unspezifisch)` |
| `Fersendekubitus` | `Dekubitus` |
| `Fersenulcus / eventuell Mischulcus` | `Ulcus cruris mixtum` |
| `Fibrinbelegtes Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `fibrinbelegtes Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Fibringbelegtes Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `gleiche Beurteilung wie Wunde 53` | `Dekubitus` |
| `Hypergranulation nach Verbrennung` | `Verbrennungswunde` |
| `Hämangiom ist ein Spezialgebiet. In der Regel ist dieses innerhalb des ersten Lebensjahres rückläufig.
Deshalb nehme ich hier keine Beurteilung vor.` | `Hämangiom ist ein Spezialgebiet. In der Regel ist dieses innerhalb des ersten Lebensjahres rückläufig.
Deshalb nehme ich hier keine Beurteilung vor.` |
| `infantiles Hämangiom,` | `infantiles Hämangiom,` |
| `Infizierte Wunden am linken Oberarm / Innenseitig` | `Infizierte Wunden am linken Oberarm / Innenseitig` |
| `Infiziertes Ulcus mit freiliegender Sehne` | `Ulkus (Ätiologie unspezifisch)` |
| `könnte arterieller Ulcus oder diabetischer Ulcus ( Angiopathie) auf Grund der Mangeldurchblutung  sein.` | `Ulkus (Ätiologie unspezifisch)` |
| `könnte diabetischer ulcus sein auf grund einer neuropathie` | `Ulkus (Ätiologie unspezifisch)` |
| `könnte ein diabetischer Fuß sein, Ulcus  nicht möglich,
traumatologische Indikation ebenso nicht ausgeschlossen` | `Ulkus (Ätiologie unspezifisch)` |
| `laterales Ulcus linker Fuß` | `Ulkus (Ätiologie unspezifisch)` |
| `massives Ulcus dekubitus` | `Dekubitus` |
| `mumifizierte Zehen (D4 und D5), gleichzeitig Nekrose an der rechten Ferse` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `möglicherweise ein feuchtes Gangrän` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `nekrotischen Wunden am Fuß` | `nekrotischen Wunden am Fuß` |
| `nekrotischer Defekt / Dekubitus` | `Dekubitus` |
| `nekrotischer Dekubitus li Ferse` | `Dekubitus` |
| `oberflächlicher Dekubitus ( 2 Stück)` | `Dekubitus` |
| `Oberflächliches Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `oberflächliches Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Oberflächliches Ulcus (diffuse Defekte)` | `Ulkus (Ätiologie unspezifisch)` |
| `offene ulcera` | `Ulkus (Ätiologie unspezifisch)` |
| `plantares ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Plantares Ulcus linker Fuß, Ursachen Klärung notwendig, bei Diabetiker Prüfung ob Neuropathisch oder Angiopathische Ursache` | `Plantares Ulcus linker Fuß, Ursachen Klärung notwendig, bei Diabetiker Prüfung ob Neuropathisch oder Angiopathische Ursache` |
| `Platzbauch nach möglichem chirurgischen Eingriff` | `Postoperative Wunde / Dehiszenz` |
| `Postoperative Wunde abdominal` | `Postoperative Wunde / Dehiszenz` |
| `pseudomas besiedeltes teils nekrotisches Ulcus.
Semizirkulär` | `Ulkus (Ätiologie unspezifisch)` |
| `rechter Fuß lateral/ malleolär` | `rechter Fuß lateral/ malleolär` |
| `schwere Nekrose am Fuß rechts lateral und plantar, offene Geschwüre über den Malleolen lateral
deutet auf arterielles Ulcus hin` | `Ulcus cruris arteriosum / Ischämisches Ulkus` |
| `schwere Ulzerationen am Fuß- mehrere offene Stellen, freiliegende Sehen, teilweise nekrotisch, belegt` | `Ulkus (Ätiologie unspezifisch)` |
| `semizirkuläres Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `semizirkuläres Ulcus re Fuß` | `Ulkus (Ätiologie unspezifisch)` |
| `superinfizierte Ulcration am rechen Fuß offene Ulcera` | `Ulkus (Ätiologie unspezifisch)` |
| `Taschenbildendes Ulcus am linken Fußrücken` | `Ulkus (Ätiologie unspezifisch)` |
| `Teils nekrotisches Ulcus an der linken Ferse.
plantares Ulcus belegt mit Infektionszeichen` | `Ulkus (Ätiologie unspezifisch)` |
| `tiefer Dekubitus` | `Dekubitus` |
| `tiefes Ulcus im Fersenbereich` | `Ulkus (Ätiologie unspezifisch)` |
| `traumatologische Wunde ( thermische Schädigung / Verbrennung 3. und 4. Grades` | `Verbrennungswunde` |
| `Ulcera rechter Fuß. könnte ursächlich diabetischer Fuß sein ( Neuropathie, Angiopathie) oder arterielles ulcus schäden auf Grund fehlender Durchblutung` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcerationen bedingt durch Vaskulitis- Form der rheumatischen Erkrankung ( Autoimmunerkrankung)` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus / warsch. Ulcus cruris, Ursache nicht klar, muss bestimmt werden` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus am Fussrücken` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus am Unterschenkel medial` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus an der Achillessehne` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus auf Grund von Mangeldurchblutung. Könnte diabetischer Fuß sein / angiopathisch bedingt.` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus auf Grund von Mangelernährung des Gewebes, Druckschäden in Kombination mit Gefäßschäden` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris` | `Ulkus (Ätiologie unspezifisch)` |
| `ulcus cruris` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris  unklarer Ursache` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris /  Gravitationsulcus: Ulcus cruris venosum` | `Ulcus cruris venosum` |
| `Ulcus cruris li lateraler Malleolus` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris möglich arteriell oder mixtum` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus cruris venosum` | `Ulcus cruris venosum` |
| `Ulcus decubitus` | `Dekubitus` |
| `Ulcus decubitus Nach Epuap Grad 2 bis 3` | `Dekubitus` |
| `Ulcus Dekubitus` | `Dekubitus` |
| `Ulcus dekubitus` | `Dekubitus` |
| `Ulcus Dekubitus Bereich OS Sacrum` | `Dekubitus` |
| `Ulcus Dekubitus Epuap Grad 3 / 4` | `Dekubitus` |
| `Ulcus dekubitus Ferse,  Stadium 3 / 4` | `Dekubitus` |
| `Ulcus Dekubitus nach Epuap Grad 2 bis 3` | `Dekubitus` |
| `Ulcus lokal abgegrenzt. belegt könnte ebenso nekrotisch sein` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus mit scheinender Hypergranulation oberhalb der Achillessehne` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus mit Stauung` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus nach Meshgraft (zumindest lässt die Struktur darauf schließen), eventuell ist die Struktur aber einer Unterdrucktherapie geschuldet` | `Postoperative Wunde / Dehiszenz` |
| `Ulcus nach Stich` | `Traumatische Wunde` |
| `Ulcus unbekannter Herkunft, könnte traumatologisch bedingte Wunde sein, durch die Wunde bei unsachgemäßer Versorgung entstehen ulcerationen ebenfalls, nicht immer Krankheitsbedingt` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus unklarer Genese` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus unklarer Genese am Bein genaue Lokalisation nicht beurteilbar` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus unklarer Genese, könnte diabet. Ulcus sein, möglich ebenso durch traumatologische Ursachen` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus unklarer Genese, könnte Venös oder arteriell oder mixum sein.
Beachte kleine Nekrose an der Ferse plantar` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus Ursache nicht genau definierbar` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus, bei vermutetem Diabetes` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus, durch die Mangelernährung ( keine Durchblutung) im Wundgebiet  könnte es sich um einen Dekubitus oder ulcus cruris handeln.` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus, Lokalisation am Bein nicht genau definierbar` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulcus. Ursache klären sollte es ein diabet. Fuß sein dann Prüfung ob angiopathisch oder neuropathisch,
Druckentlastung und Ursachenbeseitigung.` | `Ulkus (Ätiologie unspezifisch)` |
| `Ulkus an der Ferse, warsch. Dekubitus nach EPUAP  Stadium 3` | `Dekubitus` |
| `Ulkus Dekubitus am Os sacrum  nach Epuap Grad 2 / 3` | `Dekubitus` |
| `Verbrennung 2 und 3 Grades nach 9 er Regel etwa 9 % Körperoberfläche` | `Verbrennungswunde` |
| `Verbrennung 2. Grades am Bein` | `Verbrennungswunde` |
| `Verbrennung 2. und teilweise 3. Grades Oberfläche ca 9 %` | `Verbrennungswunde` |
| `Verbrennung Grad 1 bis 2 am rechten Fuß` | `Verbrennungswunde` |
| `Verbrennungswunde 1. bis 2. Grades` | `Verbrennungswunde` |
| `Verbrennungswunde am Arm Grad 2` | `Verbrennungswunde` |
| `vermutlich Mischulcus am rechten Bein, höhe der Knöchel.
Semizirkulär` | `Ulcus cruris mixtum` |
| `Wunde am li Fußrücken mit Sehnenfreilegung` | `Wunde am li Fußrücken mit Sehnenfreilegung` |
| `Wunde aufgrund einer Infusion, welche ins umliegende Gewebe ausgetreten ist` | `Wunde aufgrund einer Infusion, welche ins umliegende Gewebe ausgetreten ist` |
| `zirkuläres Ulcus Unterschenkel (vermutlich Mischulcus)` | `Ulcus cruris mixtum` |


### 2.LOKALISATION_GT_MAPPING

**Anzahl Einträge:** 134

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `...stark exsudierendes, nekrotisch belegtes Ulcus mit grünlicher Verfärbung typisch für Pseudomonas aeruginosa.` | `Enthaltung / keine Angabe` |
| `?` | `Enthaltung / keine Angabe` |
| `???` | `Enthaltung / keine Angabe` |
| `Abdomen` | `Abdomen` |
| `Abdomen, links` | `Abdomen` |
| `Arm` | `Arm / Hand` |
| `Arm oder Bein??` | `Enthaltung / keine Angabe` |
| `Aussenseitig linke Fußsohle` | `Fuß` |
| `Außenknöchel links` | `Fuß` |
| `Bein` | `Bein` |
| `Bein nicht genau definierbar` | `Bein` |
| `Bein wo genau fraglich` | `Bein` |
| `Bein, evtl. links, Unterschenkel` | `Bein` |
| `Bein, evtl. rechts, Unterschenkel` | `Bein` |
| `Bein, genaue Definition nicht möglich` | `Bein` |
| `Bein, genauere Lokalisation nicht genau definierbar` | `Bein` |
| `Bein, Unterschenkel Richtung Fuß` | `Bein` |
| `Bein, wo genau nicht definierbar` | `Bein` |
| `chronisches Ulkus im Bereich der Achillessehne
dorsaler Unterschenkel / Achillessehnenregion` | `Bein` |
| `Das Bild zeigt ein großflächiges venöses Ulcus cruris bei ausgeprägter chronisch venöser Stauung und Adipositas-assoziierter Belastung. Möglich, Oberschenkel links, Unterschenkel` | `Bein` |
| `Ferse` | `Fuß` |
| `Ferse, Achillessehne` | `Fuß` |
| `ferse, fußsohle` | `Fuß` |
| `Ferse, linker Fuß` | `Fuß` |
| `Ferse, rechter Fuß` | `Fuß` |
| `Ferse, scheint links zu sein:
gelblich-fibrinösem Belag
mäßiger Exsudation
gerötetem Wundrand` | `Fuß` |
| `fibrinösem gelblich-weißem Belag,
mäßiger Exsudation,
gerötetem Wundrand,
--> vermutlich entzündlicher bzw. kritisch kolonisierter Situation,` | `Enthaltung / keine Angabe` |
| `Fuß lateral links` | `Fuß` |
| `Fuß links plantar` | `Fuß` |
| `Fuß links plantar  lateral` | `Fuß` |
| `Fuß rechts` | `Fuß` |
| `Fuß, Ferse links` | `Fuß` |
| `Fußrücken` | `Fuß` |
| `Fußrücken linker Fuß` | `Fuß` |
| `Fußrücken rechter Fuß` | `Fuß` |
| `Fußsohle Ferse` | `Fuß` |
| `Gesäß-/perianale Region eines Säuglings` | `Gesäß / Sakral` |
| `Gesäß-/Sakralregion` | `Gesäß / Sakral` |
| `größeres, flächiges Ulcus am Unterschenkel (Wade) bei ausgeprägtem Ödem und Adipositas-assoziierter Hautveränderung.` | `Bein` |
| `keine Angabe möglich` | `Enthaltung / keine Angabe` |
| `Knöchelinnenseite` | `Fuß` |
| `könnte am linken Fuß sein... Knöchelbereich` | `Fuß` |
| `könnte der Unterschenkel sein, rechts` | `Bein` |
| `könnte Innenseite linker Fuß sein` | `Fuß` |
| `könnte oberhalb des os sacrum liegen` | `Gesäß / Sakral` |
| `könnte sich im Bereich des Steißes befinden` | `Gesäß / Sakral` |
| `könnte Unterschenkel oder Handgelenk sein` | `Enthaltung / keine Angabe` |
| `lateral linker Fuß` | `Fuß` |
| `li lateraler Malleolus` | `Fuß` |
| `li. Fußrücken` | `Fuß` |
| `linke Ferse` | `Fuß` |
| `linker Fuss` | `Fuß` |
| `linker Fussrücken` | `Fuß` |
| `linker Fuß` | `Fuß` |
| `linker Fuß
Lokalisation: dorsaler und lateraler Vorfuß mit Beteiligung der Zehenbasis` | `Fuß` |
| `linker Fuß - dorsaler Vorfuß/Fußrücken` | `Fuß` |
| `linker Fuß außen` | `Fuß` |
| `linker Fuß lateratl` | `Fuß` |
| `linker Fuß medial, malleolär` | `Fuß` |
| `linker Fuß medial-lateral 
kleine Nekrose an der Ferse außen plantar` | `Fuß` |
| `linker Fuß, Außenseite` | `Fuß` |
| `linker Fuß, außenseite` | `Fuß` |
| `linker Fuß, Ferse` | `Fuß` |
| `linker Fuß, Innenseite` | `Fuß` |
| `linker Fuß, Mittelfußsohle, Ferse` | `Fuß` |
| `linker Fuß, seite` | `Fuß` |
| `linker Fuß, Spann, Fußrücken` | `Fuß` |
| `linker Fußrücken` | `Fuß` |
| `linker Oberarm, Innenseite` | `Arm / Hand` |
| `linker Oberarm/ Innenseitig` | `Arm / Hand` |
| `linker proximaler Unterschenkel lateral` | `Bein` |
| `linkes Bein unterhalb Knie lateral` | `Bein` |
| `lokalisation nicht genau zu definieren` | `Enthaltung / keine Angabe` |
| `Lokalisation: Fußrücken, lateraler Vorfuß sowie Zehenbereiche` | `Fuß` |
| `Lokalisation: lateraler Mittelfuß/Knöchelbereich` | `Fuß` |
| `Lokalisation: lateraler Vor-/Mittelfuß` | `Fuß` |
| `Lokalisation: sakrogluteale/perianale Region beidseits` | `Gesäß / Sakral` |
| `Lokalisation: Unterschenkelbereich` | `Bein` |
| `Lokalisation: Unterschenkelregion` | `Bein` |
| `Lokalisation: vermutlich Sakral-/Gesäßregion` | `Gesäß / Sakral` |
| `mediale Fußseite linker Fuß` | `Fuß` |
| `mehrere kleine bis mittelgroße Ulzerationen am Unterschenkel (Wade, rechts?) mit entzündlich wirkender Umgebungshaut.` | `Bein` |
| `multiple Schädigung gesamter Gesäßbereich` | `Gesäß / Sakral` |
| `nicht beurteilbar` | `Enthaltung / keine Angabe` |
| `nicht genau definierbar` | `Enthaltung / keine Angabe` |
| `nicht genau definierbar könnte Sakralbereich sein` | `Gesäß / Sakral` |
| `nicht genau definierbar sieht für mich aus wie am Vorfuß` | `Fuß` |
| `nicht genau definierbar, meist am Unterschenkel` | `Bein` |
| `nicht genau definierbar, Vermutung Unterschenkel` | `Bein` |
| `Oberarb Muskulus bizeps` | `Arm / Hand` |
| `oberhalb der Achillessehne` | `Fuß` |
| `Os Sacrum` | `Gesäß / Sakral` |
| `plantarseitig rechter Fuß` | `Fuß` |
| `re Fuß` | `Fuß` |
| `rechte Ferse` | `Fuß` |
| `rechte Hand` | `Arm / Hand` |
| `rechte Hand und Arm` | `Arm / Hand` |
| `rechter Fuß` | `Fuß` |
| `rechter Fuß - lateraler und plantarer Fußbereich/Ferse` | `Fuß` |
| `rechter Fuß Fußrücken und lateral` | `Fuß` |
| `rechter Fuß medial, Richtung plantar.` | `Fuß` |
| `rechter Fuß plantar` | `Fuß` |
| `rechter Fuß, Ferse` | `Fuß` |
| `rechter Fuß, Ferse, Mittelfuß - Fußsohle` | `Fuß` |
| `rechter Fuß, Fußsohle` | `Fuß` |
| `rechter Fuß, in Höhe der großen Zehe, unterhalb der medialen Malleolen` | `Fuß` |
| `rechter Fuß, Innenseite, Knöchel` | `Fuß` |
| `rechter Fuß, Spann` | `Fuß` |
| `rechter Unterarm, rechtes Handgelenk, rechte Hand` | `Arm / Hand` |
| `rechter Unterschenkel` | `Bein` |
| `rechtes Bein, höhe der Knöchel` | `Bein` |
| `rechtes Bein, Kniebereich, Unterschenkel` | `Bein` |
| `Rima Ani` | `Gesäß / Sakral` |
| `sacralbereich` | `Gesäß / Sakral` |
| `Sakralbereich` | `Gesäß / Sakral` |
| `Sakralbereich linke hälfte` | `Gesäß / Sakral` |
| `Sakraler Bereich` | `Gesäß / Sakral` |
| `sakrales Dekubitalulkus` | `Gesäß / Sakral` |
| `schwer zu beurteilen, keine genaue Angabe möglich,
eventuell Rücken Richtung Oberarm /` | `Enthaltung / keine Angabe` |
| `schwer zu beurteilen, Vermutung am Trochanter major` | `Bein` |
| `schwierig zu beantworten... könnte die Wade sein, evtl. rechts` | `Bein` |
| `Steiß` | `Gesäß / Sakral` |
| `Unterarm` | `Arm / Hand` |
| `Unterschenkel` | `Bein` |
| `unterschenkel` | `Bein` |
| `Unterschenkel  medial` | `Bein` |
| `Unterschenkel warsch. gamaschenartig / bereits zirkulierend` | `Bein` |
| `Unterschenkel weit umfassend` | `Bein` |
| `Unterschenkel, Außenseite auf Knie Höhe` | `Bein` |
| `Unterschenkel, rechts, Innenseite` | `Bein` |
| `Unterschenkel/Knöchelregion, zirkumferenziell ausgedehnt` | `Bein` |
| `Unterschenkel?` | `Bein` |
| `vermutlich am Außenknöchel` | `Fuß` |
| `vermutlich am Unterschenkel` | `Bein` |


### 2.EXSUDAT_GT_MAPPING

**Anzahl Einträge:** 62

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Annahme stark` | `Stark` |
| `blutig bis serös teilweise vorhanden dann eher mäßig` | `Mäßig` |
| `eher schwach b is mäßig` | `Leicht`, `Mäßig` |
| `eher wenig` | `Leicht` |
| `eher weniger` | `Leicht` |
| `gering bis gar nicht` | `Keine`, `Leicht` |
| `Große Wunde: stark, da Mazerationen am Wundrand
Kleine Nekrose: trocken` | `Stark` |
| `kein` | `Keine` |
| `Keine` | `Keine` |
| `keine` | `Keine` |
| `keine Angabe möglich` | `Enthaltung / keine Angabe` |
| `keine Angabe möglich / eher wenig` | `Leicht` |
| `keine Angabe möglich / vermutlich mässig` | `Mäßig` |
| `keine Angabe möglich / vermutlich wenig` | `Leicht` |
| `keine Angabe möglich, vermutlich gering` | `Leicht` |
| `keine Angabe möglich, vermutlich trocken` | `Keine` |
| `keine Einschätzung möglich` | `Enthaltung / keine Angabe` |
| `keine genaue Angabe möglich, sieht eher trocken bis leicht exsudierend aus` | `Keine`, `Leicht` |
| `könnte eher schwach sein` | `Leicht` |
| `Leicht` | `Leicht` |
| `leicht` | `Leicht` |
| `leicht bis mittel` | `Leicht`, `Mäßig` |
| `leicht bis mäßig` | `Leicht`, `Mäßig` |
| `leichte bis mäßige exsudation` | `Leicht`, `Mäßig` |
| `mittel` | `Mäßig` |
| `mittel bis stark` | `Mäßig`, `Stark` |
| `mittelstark` | `Mäßig` |
| `mäfig` | `Mäßig` |
| `Mässig` | `Mäßig` |
| `Mäßig` | `Mäßig` |
| `mäßig` | `Mäßig` |
| `mäßig bis stark` | `Mäßig`, `Stark` |
| `mäßig bis stark, sicher ist eine Geruchsbildung süßlich aromatisch teilweise beschrieben als traubenartig` | `Mäßig`, `Stark` |
| `Nekrosen: kein Exsudat. Unterschenkel mäßig` | `Mäßig` |
| `nicht beurteilbar` | `Enthaltung / keine Angabe` |
| `nicht beurteilbar, vermutlich stark` | `Stark` |
| `nicht genau definierbar, aus der Erfahrung heraus mäßige Exsudation` | `Mäßig` |
| `nicht klar, eher trübe Wunde könnte Geruch abgeben` | `Enthaltung / keine Angabe` |
| `nicht zu beschreiben` | `Enthaltung / keine Angabe` |
| `offenen stelle mäßig, geschlossene stelle kein bis wenig exsudat` | `Keine`, `Leicht` |
| `scheint mäßig zu sein` | `Mäßig` |
| `schwach` | `Leicht` |
| `schwach bin mäßig` | `Leicht`, `Mäßig` |
| `schwach bis mäßig` | `Leicht`, `Mäßig` |
| `schwach bis nicht vorhanden` | `Keine`, `Leicht` |
| `sehr gering` | `Leicht` |
| `Stark` | `Stark` |
| `stark` | `Stark` |
| `vermutlich gering` | `Leicht` |
| `vermutlich hoch` | `Stark` |
| `vermutlich hohe Exsudation` | `Stark` |
| `vermutlich kaum` | `Keine` |
| `vermutlich mittel` | `Mäßig` |
| `vermutlich mittelmässig` | `Mäßig` |
| `vermutlich mittelmäßig` | `Mäßig` |
| `vermutlich mässig` | `Mäßig` |
| `vermutlich mäßig` | `Mäßig` |
| `vermutlich starke Exsudation` | `Stark` |
| `vermutlich vorhanden, in welcher Menge ist nicht zu beurteilen` | `Enthaltung / keine Angabe` |
| `vermutlich wenig` | `Leicht` |
| `wahrscheinlich mittelmäßig vorhanden` | `Mäßig` |
| `warsch hoch bis sehr hoch,  klare exsudation` | `Stark` |


### 2.WUNDUMGEBUNG_GT_MAPPING

**Anzahl Einträge:** 38

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `["atrophisch-trockene Haut mit trophischen Störungen","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)` |
| `["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)","Erythem / Rötung"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Erythem / Rötung` |
| `["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)` |
| `["Ekzem / Dermatitis","Erythem / Rötung"]` | `Ekzem / Dermatitis`, `Erythem / Rötung` |
| `["Ekzem / Dermatitis"]` | `Ekzem / Dermatitis` |
| `["empfindliche Säuglingshaut mit hoher Feuchtigkeits- und Reibungsbelastung"]` | `Sonstiges` |
| `["Erythem / Rötung","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Erythem / Rötung` |
| `["Erythem / Rötung","deutliche entzündliche Rötung der Umgebung"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","eher trocken wirkende Umgebung"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","Ekzem / Dermatitis","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Ekzem / Dermatitis`, `Erythem / Rötung` |
| `["Erythem / Rötung","Ekzem / Dermatitis"]` | `Ekzem / Dermatitis`, `Erythem / Rötung` |
| `["Erythem / Rötung","entzündliche Umgebungshaut"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","leicht gerötete, glänzende Umgebungshaut"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","Mazeration","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Erythem / Rötung`, `Mazeration` |
| `["Erythem / Rötung","Mazeration"]` | `Erythem / Rötung`, `Mazeration` |
| `["Erythem / Rötung","Weichteilreizung"]` | `Erythem / Rötung` |
| `["Erythem / Rötung","Ödem","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Erythem / Rötung`, `Ödem` |
| `["Erythem / Rötung","Ödem"]` | `Erythem / Rötung`, `Ödem` |
| `["Erythem / Rötung"]` | `Erythem / Rötung` |
| `["fragile, atrophe Haut"]` | `Sonstiges` |
| `["gerötet-glänzende Haut, Hinweis auf chronische venöse Stauung/Ödemneigung"]` | `Erythem / Rötung`, `Ödem` |
| `["gerötet-glänzende, ödematöse Haut","Erythem / Rötung"]` | `Erythem / Rötung`, `Ödem` |
| `["gut durchbluteter, überwiegend roter Wundgrund"]` | `Reizlos / intakt` |
| `["Keratosen"]` | `Sonstiges` |
| `["Mazeration","Erythem / Rötung","trockener wirkende Areale mit verminderter Durchblutung"]` | `Erythem / Rötung`, `Mazeration` |
| `["Mazeration","Erythem / Rötung"]` | `Erythem / Rötung`, `Mazeration` |
| `["Mazeration","glänzend"]` | `Mazeration` |
| `["Mazeration","glänzende, gespannte Umgebungshaut"]` | `Mazeration` |
| `["Mazeration"]` | `Mazeration` |
| `["Reizlos / intakt","Erythem / Rötung"]` | `Erythem / Rötung`, `Reizlos / intakt` |
| `["Reizlos / intakt"]` | `Reizlos / intakt` |
| `["rocken, teils schuppig, gespannt"]` | `Sonstiges` |
| `["zahlreiche erythematöse Makulae/Papeln, livid-entzündliche Hautveränderungen, Hinweis auf entzündlich-vaskulären Prozess"]` | `Ekzem / Dermatitis`, `Erythem / Rötung` |
| `["Ödem","CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"]` | `CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)`, `Ödem` |
| `["Ödem","Erythem / Rötung"]` | `Erythem / Rötung`, `Ödem` |
| `["Ödem","gespannte, trophisch veränderte Haut"]` | `Ödem` |
| `["Ödem"]` | `Ödem` |
| `[]` |  |


### 2.WUNDRAND_GT_MAPPING

**Anzahl Einträge:** 33

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `["Epibolie (eingerollter Wundrand)","Gerötet / entzündlich","Mazeriert"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich`, `Mazeriert` |
| `["Epibolie (eingerollter Wundrand)","Gerötet / entzündlich"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich` |
| `["Epibolie (eingerollter Wundrand)","Mazeriert"]` | `Epibolie (eingerollter Wundrand)`, `Mazeriert` |
| `["Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)` |
| `["Gelbliche fibrinöse Randbeläge"]` |  |
| `["Gerötet / entzündlich","Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","glänzende, ödematöse Haut"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","livid-erythematöse Hautveränderungen"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","Mazeriert","Unterminiert (Wundtaschen)"]` | `Gerötet / entzündlich`, `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Gerötet / entzündlich","Mazeriert"]` | `Gerötet / entzündlich`, `Mazeriert` |
| `["Gerötet / entzündlich","relativ scharf begrenzte Wundränder"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","Taschenbildung möglich"]` | `Gerötet / entzündlich`, `Unterminiert (Wundtaschen)` |
| `["Gerötet / entzündlich","unregelmäßige Wundränder"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","unregelmäßigen Rändern"]` | `Gerötet / entzündlich` |
| `["Gerötet / entzündlich","Unterminiert (Wundtaschen)"]` | `Gerötet / entzündlich`, `Unterminiert (Wundtaschen)` |
| `["Gerötet / entzündlich"]` | `Gerötet / entzündlich` |
| `["Hyperkeratotisch","Gerötet / entzündlich"]` | `Gerötet / entzündlich`, `Hyperkeratotisch` |
| `["Hyperkeratotisch"]` | `Hyperkeratotisch` |
| `["Mazeriert","Epibolie (eingerollter Wundrand)","Gerötet / entzündlich"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich`, `Mazeriert` |
| `["Mazeriert","Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)`, `Mazeriert` |
| `["Mazeriert","Gerötet / entzündlich","Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)`, `Gerötet / entzündlich`, `Mazeriert` |
| `["Mazeriert","Gerötet / entzündlich","Unterminiert (Wundtaschen)"]` | `Gerötet / entzündlich`, `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Mazeriert","Gerötet / entzündlich"]` | `Gerötet / entzündlich`, `Mazeriert` |
| `["Mazeriert","teilweise aufgequollen"]` | `Mazeriert` |
| `["Mazeriert","Unterminiert (Wundtaschen)","Gerötet / entzündlich"]` | `Gerötet / entzündlich`, `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Mazeriert","Unterminiert (Wundtaschen)"]` | `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Mazeriert"]` | `Mazeriert` |
| `["Reizlos / unauffällig"]` | `Reizlos / unauffällig` |
| `["scharf begrenzt, teils livide/verfärbt, ischämietypisch"]` | `Reizlos / unauffällig` |
| `["Unterminiert (Wundtaschen)","Epibolie (eingerollter Wundrand)"]` | `Epibolie (eingerollter Wundrand)`, `Unterminiert (Wundtaschen)` |
| `["Unterminiert (Wundtaschen)","Gerötet / entzündlich"]` | `Gerötet / entzündlich`, `Unterminiert (Wundtaschen)` |
| `["Unterminiert (Wundtaschen)","Mazeriert"]` | `Mazeriert`, `Unterminiert (Wundtaschen)` |
| `["Unterminiert (Wundtaschen)"]` | `Unterminiert (Wundtaschen)` |


### 2.LOKALISATION_KEYWORDS

**Anzahl Einträge:** 10

| Eingabe / Rohbegriff (Freitext / Synonym) | Gemappter Zielbegriff (Normalisiert) |
| :--- | :--- |
| `Abdomen` | `abdomen`, `bauch`, `peristom`, `stoma` |
| `Arm` | `arm`, `ellenbogen`, `oberarm`, `unterarm`, `bizeps`, `axilla`, `achsel` |
| `Bein` | `bein`, `knöchel`, `unterschenkel`, `oberschenkel`, `knie`, `gaiter` |
| `Brust` | `brust`, `thorax` |
| `Flanke` | `flanke` |
| `Fuß` | `fuß`, `fuss`, `zehe`, `ferse`, `fußsohle`, `fußrücken`, `plantar`, `vorfuß`, `rückfuß`, `malleol`, `achillessehne`, `calcaneus`, `hallux`, `metatarsal` |
| `Gesäß` | `gesäß`, `sakral`, `kreuzbein`, `steißbein`, `os sacrum`, `sacral`, `rima ani`, `steiß`, `trochanter`, `gluteal`, `paraglutäal` |
| `Hand` | `\bhand\b`, `\bhände\b`, `finger`, `handgelenk`, `handrücken` |
| `Kopf` | `\bkopf\b`, `hals`, `nacken` |
| `Rücken` | `(?<!fuß)(?<!fuss)(?<!hand)(?<!händ)rücken` |

