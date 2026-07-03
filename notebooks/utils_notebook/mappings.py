SPELLING_MAPPING = {
    "ulcus": "ulkus",
    "decubitus": "dekubitus",
}

WUNDTYP_GT_MAPPING = {
    # Basis-Mappings
    "Ulcus": ["Ulkus"],
    "Ulkus": ["Ulkus"],
    "ulcus": ["Ulkus"],
    "ulkus": ["Ulkus"],
    
    # Spezifische Mappings
    "durch Insektenstich": ["Traumatische Wunde"],
    "chronisches Ulkus cruris": ["Ulkus cruris"],
    "chronisches Ulcus cruris": ["Ulkus cruris"],
    "nekrotische Ischämische Fußwunde / Gangrän": ["Ischämisches Fußulkus (Gangrän)"],
    "nekrotische ischämische Fußwunde / Gangrän": ["Ischämisches Fußulkus (Gangrän)"],
    "Ischämische Nekrose/Gangrän des Fußes": ["Ischämisches Fußulkus (Gangrän)"],
    "Ischämische Nekrose / drohende Gangrän am Fuß": ["Ischämisches Fußulkus (Gangrän)"],
    "Ischämische Nekrose / Gangrän am Fuß": ["Ischämisches Fußulkus (Gangrän)"],
    "chronische Fußwunde / Ulkus": ["Fußulkus"],
    "chronische Fußwunde / Ulcus": ["Fußulkus"],
    "ausgedehnte, tiefe, nekrotische Ulzeration": ["Ulzeration"],
    "Fußulkus (Ätiologie unklar, Bildbefund)": ["Fußulkus"],
    "Fußulkus unklare Ätiologie (DD: traumatisch/diabetisch/arteriell)": ["Fußulkus"],
    "multiple infizierte chronische Fußulzera": ["Fußulkus"],
    "Multiple oberflächliche Ulzera am Fußrücken": ["Fußulkus"],
    "chronisches Ulkus": ["Ulkus"],
    "chronisches Ulcus": ["Ulkus"],
    "Ulkus Fußrücken mit deutlicher Gewebedestruktion und freiliegender Sehnenstruktur": ["Fußulkus"],
    "Ulcus Fußrücken mit deutlicher Gewebedestruktion und freiliegender Sehnenstruktur": ["Fußulkus"],
    "neuroischämisches bzw. arterielles Fußulkus": ["arterielles/ ischämisches Fußulkus"],
    "neuroischämisches bzw. arterielles Fußulcus": ["arterielles/ ischämisches Fußulkus"],
    "multiple kleine Ulzera": ["Ulzera"],
    "großflächiges, flaches chronisches Ulkus": ["Ulkus"],
    "großflächiges, flaches chronisches Ulcus": ["Ulkus"],
    "kleines, oberflächliches Ulkus": ["Ulkus"],
    "kleines, oberflächliches Ulcus": ["Ulkus"],
    "ausgedehntes, tiefes chronisches Ulkus": ["Ulkus"],
    "ausgedehntes, tiefes chronisches Ulcus": ["Ulkus"],
    "rundlich-ovales Ulkus": ["Ulkus"],
    "rundlich-ovales Ulcus": ["Ulkus"],
    "ausgeprägtes infiziertes Ulcus cruris, Ulcus cruris venosum": ["Ulkus cruris venosum"],
    "Adipositas-assoziiert": ["Ulkus cruris venosum"],
    "tiefer reichende Ulzerationen am Unterschenkel mit chronisch entzündlicher Umgebung": ["Ulzeration"],
    "vaskulitischen Ulzera": ["vaskulitische Ulzera"],
    "mit deutlichen Zeichen einer lokalen Infektion und chronisch entzündlicher Hautveränderungen": ["Diabetisches Fußulkus"],
    "hochgradig destruierende Fußwunde": ["Diabetisches Fußulkus"]
}

WUNDUMGEBUNG_GT_MAPPING = {
    # Hier können Mappings für die Wundumgebung eingetragen werden, z. B.:
    # "eher trocken wirkende Umgebung": ["trocken"],
    "deutliche entzündliche Rötung der Umgebung": ["Erythem / Rötung"],
    "entzündliche Umgebungshaut": ["Erythem / Rötung"],
    "leicht gerötete, glänzende Umgebungshaut": ["Erythem / Rötung"],
    "gerötet-glänzende, ödematöse Haut, Erythem / Rötung": ["Erythem / Rötung"],
    "Mazeration, glänzende, gespannte Umgebungshaut": ["Mazeration"]
}

WUNDRAND_GT_MAPPING = {
    # Hier können Mappings für den Wundrand eingetragen werden, z. B.:
    # "mazerierter Wundrand": ["Mazeriert"],
    "Gerötet / entzündlich, unregelmäßige Wundränder": ["Gerötet / entzündlich"],
    "Gerötet / entzündlich, livid-erythematöse Hautveränderungen": ["Gerötet / entzündlich"],
    "Gerötet / entzündlich, unregelmäßigen Rändern": ["Gerötet / entzündlich"],
    "Gerötet / entzündlich, relativ scharf begrenzte Wundränder": ["Gerötet / entzündlich"],
    "Mazeriert, teilweise aufgequollen": ["Mazeriert"]
}

SEKUNDAERVERBAND_GT_MAPPING = {
    # Hier können Mappings für den Sekundärverband eingetragen werden, z. B.:
    # "saugfähiger Schaumverband": ["Schaumstoffverband"],
    # → Schaumstoffverbände
    "Schaumverbände": ["Schaumstoffverbände"],
    "Schaumverband": ["Schaumstoffverbände"],
    "saugfähiger Schaumverband": ["Schaumstoffverbände"],
    "atraumatischer Schaumverband": ["Schaumstoffverbände"],
    "absorbierender Schaumverband": ["Schaumstoffverbände"],
    "saugfähiger Schaumverband, atraumatische Fixierung": ["Schaumstoffverbände, atraumatische Fixierung"],
    "absorbierender Schaumverband, atraumatische Fixierung": ["Schaumstoffverbände, atraumatische Fixierung"],
    "atraumatische Schaumverbände, ggf. Unterdrucktherapie (VAC) nach Débridement": ["Schaumstoffverbände, Unterdrucktherapie (VAC)"],
    "PU-Schaumverband, Atraumatische Fixierung": ["Schaumstoffverbände, atraumatische Fixierung"],
    "weicher PU-Schaumverband, weicher PU-Schaumverband": ["Schaumstoffverbände"],
    "Elastische Fixierbinden, dünner PU-Schaumverband": ["Schaumstoffverbände, Elastische Fixierbinden"],

    # → Superabsorber, Schaumstoffverbände
    "Superabsorber, hochabsorbierender PU-Schaumverband": ["Superabsorber, Schaumstoffverbände"],
    "Superabsorber oder PU-Schaumverband": ["Superabsorber, Schaumstoffverbände"],
    "Superabsorber weicher PU-Schaumverband": ["Superabsorber, Schaumstoffverbände"],
    "Superabsorber, hochabsorbierende Schaumverbände": ["Superabsorber, Schaumstoffverbände"],
    "PU-Schaumverband oder Superabsorber": ["Superabsorber, Schaumstoffverbände"],

    # → Schaumstoffverbände, Superabsorber bei stärkerer Exsudation
    "absorbierender Schaumverband, Superabsorber bei stärkerer Sekretion": ["Schaumstoffverbände, Superabsorber bei stärkerer Exsudation"],
    "weicher PU-Schaumverband Superabsorber bei stärkerem Exsudat": ["Schaumstoffverbände, Superabsorber bei stärkerer Exsudation"],
    "PU-Schaumverband oder Superabsorber bei stärkerer Exsudation": ["Schaumstoffverbände, Superabsorber bei stärkerer Exsudation"],
    "PU-Schaumverband, bei stärkerem Exsudat: Superabsorber": ["Schaumstoffverbände, Superabsorber bei stärkerer Exsudation"],
    "PU-Schaumverband oder kleiner Superabsorber bei stärkerer Sekretion": ["Schaumstoffverbände, Superabsorber bei stärkerer Exsudation"],
    "PU-Schaumverband, Superabsorber bei stärkerer Sekretion": ["Schaumstoffverbände, Superabsorber bei stärkerer Exsudation"],
    "kleiner PU-Schaumverband oder weicher Superabsorber bei stärkerer Exsudation": ["Schaumstoffverbände, Superabsorber bei stärkerer Exsudation"],
    "Superabsorber ergänzen": ["Schaumstoffverbände, Superabsorber bei stärkerer Exsudation"],

    # → Schaumstoffverbände, sterile Polsterung
    "weicher PU-Schaumverband,absorbierende sterile Sekundärauflagen": ["Schaumstoffverbände, sterile Polsterung"],
    "silikonisierter Schaumverband, absorbierende sterile Auflagen": ["Schaumstoffverbände, sterile Polsterung"],
    "weicher absorbierender Schaumverband sterile Saugkompressen": ["Schaumstoffverbände, sterile Polsterung"],
    "weicher PU-Schaumverband, sterile Polsterung": ["Schaumstoffverbände, sterile Polsterung"],
    "silikonisierter Schaumverband, absorbierender PU-Schaumverband": ["Schaumstoffverbände"],

    # → Schaumstoffverbände, druckentlastende Polsterung
    "weicher PU-Schaumverband, druckentlastende Polsterung": ["Schaumstoffverbände, druckentlastende Polsterung"],
    "weicher PU-Schaumverband druckreduzierende Polsterung": ["Schaumstoffverbände, druckentlastende Polsterung"],
    "weicher PU-Schaumverband, druckreduzierende Polsterung, ggf. Superabsorber": ["Schaumstoffverbände, druckentlastende Polsterung, Superabsorber"],

    # → Superabsorber
    "stark saugfähige Superabsorber": ["Superabsorber"],

    # → abhängig von Kompressionstherapie
    "abhängig von der Kompressionstherapie": ["abhängig von Kompressionstherapie"],
    "abhängig von Kompressionstherapie": ["abhängig von Kompressionstherapie"],
    "über Kompression": ["abhängig von Kompressionstherapie"],
    "Kompressionstherapie": ["abhängig von Kompressionstherapie"],
    "kommt auf die Kompression an": ["abhängig von Kompressionstherapie"],

    # → abhängig von Druckentlastung
    "abhängig von Druckentlastung": ["abhängig von Druckentlastung"],
    "abhängig von der Druckentlastung": ["abhängig von Druckentlastung"]
}

PRODUKT_GT_MAPPING = {
    # Hier können Mappings für Präferenz- und Alternativprodukte eingetragen werden, z. B.:
    # "Alginate": ["Alginat"],
    "Schaumstoffverbände (Foam)": ["Schaumstoffverbände"],

    # Silber entfernt → Basisklasse
    "Silberhydrofaser": ["Hydrofaser / Hydrofiber"],
    "Hydrofaser / Hydrofiber, silberhaltige Varianten bei bakterieller Belastung": ["Hydrofaser / Hydrofiber"],
    "Hydrofaser / Hydrofiber, Wundkontaktschichten (Silikon/Paraffin), Bei bakterieller Belastung: silberhaltige Varianten kurzfristig": ["Hydrofaser / Hydrofiber, Wundkontaktschichten (Silikon/Paraffin)"],
    "Alginate, Hydrofaser / Hydrofiber, bei kritischer Kolonisation silberhaltige Varianten erwägen": ["Hydrofaser / Hydrofiber, Alginate"],
    "Hydrofaser / Hydrofiber, Schaumstoffverbände (Foam), Silber-Schaumverbände": ["Hydrofaser / Hydrofiber, Schaumstoffverbände"],
    "Hydrofaser / Hydrofiber, Bei Infektionsverdacht silberhaltige Varianten, Schaumstoffverbände (Foam)": ["Hydrofaser / Hydrofiber, Schaumstoffverbände"],
    "Schaumstoffverbände (Foam), silberhaltige Verbrennungsauflagen": ["Schaumstoffverbände, Verbrennungsauflagen"],
    "antiseptische Wundauflagen --> Silber PHMB-haltige Produkte": ["PHMB-haltige Produkte"],

    "silberhaltige Produkte kurzfristig": ["Hydrofaser / Hydrofiber"],
    "Silberhydrofaser oder Silberalginat": ["Hydrofaser / Hydrofiber, Alginate"],
    "Silberalginate, Silberhydrofaser": ["Hydrofaser / Hydrofiber, Alginate"],
    "Silberhydrofaser, Silberalginat": ["Hydrofaser / Hydrofiber, Alginate"],
    "Silberhydrofaser, antimikrobielle Alginate": ["Hydrofaser / Hydrofiber, Alginate"],
    "silberhydrofaser/Silberalginat bei kritischer Kolonisation": ["Hydrofaser / Hydrofiber, Alginate"],
    "Silberalginat, antimikrobielle Alginate ggf. PHMB-haltige Wundauflagen": ["Alginate, PHMB-haltige Wundauflagen"],
    "Bei feuchten/infizierten Bereichen: Silberhydrofaser Silberalginat antimikrobielle Wundauflagen.": ["Hydrofaser / Hydrofiber, Alginate"],
    "Bei kritischer Kolonisation:  Silberhydrofaser kurzfristig, Hydrogele (Kompresse)": ["Hydrofaser / Hydrofiber, Hydrogele (Kompresse)"],
    "Alginate bei stärker exsudierend": ["Alginate"],
    "ggf. Hydrogel bei trockeneren Belägen": ["Hydrogele (Kompresse)"],
    "Alginate, Hydrofaser / Hydrofiber, Superabsorber, ggf. Unterdrucktherapie (NPWT/VAC) nach Nekrosensanierung": ["Alginate, Hydrofaser / Hydrofiber, Superabsorber, Unterdrucktherapie (NPWT/VAC)"],

    # Trockene-Nekrose-Schutzverbände normalisiert (Silber entfernt)
    "trockene sterile Schutzverbände, atraumatische Kontaktlagen, keine aggressive Befeuchtung der stabilen Nekrose": ["trockene sterile Schutzverbände, Wundkontaktschichten (Silikon/Paraffin)"],
    "Bei trockener Nekrose: trockener Schutzverband atraumatische Kontaktlagen.": ["trockene sterile Schutzverbände, Wundkontaktschichten (Silikon/Paraffin)"],
    "trockene sterile Abdeckung, atraumatische Schutzverbände, keine aggressive Befeuchtung": ["trockene sterile Schutzverbände"],
    "Bei trockenen Nekrosen: atraumatische trockene Schutzverbände, Bei feuchten/infizierten Bereichen: Silberhydrofaser Silberalginat antimikrobielle Wundauflagen": ["trockene sterile Schutzverbände, Hydrofaser / Hydrofiber, Alginate"],

    # Wundtyp-abhängig → Produkte behalten
    "Hydrogel bei trockenen Nekroseanteilen, Hydrofaser oder Alginat bei Exsudat": ["Hydrogele (Kompresse), Hydrofaser / Hydrofiber, Alginate"],
}

DEBRIDEMENT_GT_MAPPING = {
    # Hier können Mappings für das Débridement eingetragen werden, z. B.:
    # "chirurgisches Debridement": ["Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), vorsichtige mechanische Reinigung lockerer Beläge": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), vorsichtig mechanisches Debridement": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "nicht aggressiv entfernen, solange keine Revaskularisation erfolgt ist, Chirurgisch/Scharf (Skalpell, Kürette)": ["Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), chirurgisches Debridement erst nach Perfusionsverbesserung, sofern möglich": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Chirurgisch/Scharf (Skalpell, Kürette), autolytisches Debridement, enzymatisches Debridement - ergänzend": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette), Enzymatisch"],
    "konservatives Abwarten bei unklarer Demarkation, selektives chirurgisches Débridement, enzymatisch/autolytisch ergänzend": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette), Enzymatisch"],
    "kein aggressives Debridement ohne Gefäßstatus, trockene stabile Nekrosen ggf. belassen, Bei infizierten/fibrinösen Belägen: zurückhaltendes scharfes Debridement, autolytische Verfahren möglich": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette)"],

    "Autolytisch (Hydrogele, Folienverbände), Hydrokolloide": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)"],
    "Autolytisch (Hydrogele, Folienverbände), Hydrokolloide, Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "Autolytisch (Hydrogele, Chirurgisch/Scharf (Skalpell, Folienverbände), Hydrokolloide, Kürette), Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung), Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Chirurgisch/Scharf (Skalpell, Kürette), Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen": ["Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung), Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette), Enzymatisch": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette), Enzymatisch"],
    "Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen": ["Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "Autolytisch (Hydrogele, Chirurgisch/Scharf (Skalpell, Folienverbände), Hydrokolloide, Kürette)": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette)"],
}

LOKALISATION_KEYWORDS = {
    "Fuß": ["fuß", "fus", "ferse", "knöchel", "zehe", "spann", "sohle", "plantar", "vorfuß", "mittelfuß",
            "fußrücken", "sprunggelenk", "malleolar", "malleol", "dorsolateral", "dorsalseitig", "rückfuß",
            "großzehe", "calcaneus", "außenknöchel"],
    "Bein": ["bein", "schenkel", "wade", "knie", "achilles", "knöchelregion",
             "unterschenkel", "gaiter"],
    "Arm": ["arm", "oberarm", "unterarm"],
    "Hand": ["hand", "handgelenk"],
    "Abdomen": ["abdomen", "bauch", "bauchdecke", "abdominal"],
    "Gesäß/Steiß": ["gesäß", "gesaess", "sakral", "steiß", "steiss", "perianal", "sakrogluteal",
                    "gluteal", "intergluteal"],
}
