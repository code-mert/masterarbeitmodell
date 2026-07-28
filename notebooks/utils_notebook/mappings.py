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
    "Dekubitus": ["Dekubitus"],
    "Diabetisches Fußulkus": ["Diabetisches Fußulkus"],
    "Postoperative Wunde": ["Postoperative Wunde"],
    "Traumatische Wunde": ["Traumatische Wunde"],
    "Verbrennungswunde": ["Verbrennungswunde"],
    "Ulkus cruris venosum": ["Ulkus cruris venosum"],
    "Ulcus cruris venosum": ["Ulkus cruris venosum"],
    "Ulkus cruris": ["Ulkus cruris"],
    "ausgeprägtes infiziertes Ulcus cruris": ["Ulkus cruris"],
    "ischämisches Ulkus": ["ischämisches Ulkus"],
    
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
    # Schema-Standardwerte & direkte Synonyme
    "Erythem / Rötung": ["Erythem / Rötung"],
    "Mazeration": ["Mazeration"],
    "Ödem": ["Ödem"],
    "CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)": ["CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"],
    
    # Entzündung / Rötung Phrasen
    "deutliche entzündliche Rötung der Umgebung": ["Erythem / Rötung"],
    "entzündliche Umgebungshaut": ["Erythem / Rötung"],
    "leicht gerötete, glänzende Umgebungshaut": ["Erythem / Rötung"],
    "gerötet-glänzende, ödematöse Haut, Erythem / Rötung": ["Erythem / Rötung"],
    "gerötet-glänzende Haut, Hinweis auf chronische venöse Stauung/Ödemneigung": ["Erythem / Rötung", "Ödem"],
    "gerötet-glänzende, ödematöse Haut": ["Erythem / Rötung", "Ödem"],
    
    # Mazeration Phrasen
    "Mazeration, glänzende, gespannte Umgebungshaut": ["Mazeration"],
    "glänzende, gespannte Umgebungshaut": ["Mazeration"],
}

WUNDRAND_GT_MAPPING = {
    # Schema-Standardwerte
    "Gerötet / entzündlich": ["Gerötet / entzündlich"],
    "Mazeriert": ["Mazeriert"],
    "Unterminiert (Wundtaschen)": ["Unterminiert (Wundtaschen)"],
    "Reizlos / unauffällig": ["Reizlos / unauffällig"],
    "Hyperkeratotisch": ["Hyperkeratotisch"],
    "Epibolie (eingerollter Wundrand)": ["Epibolie (eingerollter Wundrand)"],

    # Rötung / Entzündung Varianten
    "Gerötet / entzündlich, unregelmäßige Wundränder": ["Gerötet / entzündlich"],
    "Gerötet / entzündlich, livid-erythematöse Hautveränderungen": ["Gerötet / entzündlich"],
    "Gerötet / entzündlich, unregelmäßigen Rändern": ["Gerötet / entzündlich"],
    "Gerötet / entzündlich, relativ scharf begrenzte Wundränder": ["Gerötet / entzündlich"],
    "livid-erythematöse Hautveränderungen": ["Gerötet / entzündlich"],

    # Mazeriert Varianten
    "Mazeriert, teilweise aufgequollen": ["Mazeriert"],
    "teilweise aufgequollen": ["Mazeriert"],
}

SEKUNDAERVERBAND_GT_MAPPING = {
    # Schema-Standardwerte & Synonyme
    "Schaumstoffverbände (Foam)": ["Schaumstoffverbände (Foam)"],
    "Schaumstoffverbände": ["Schaumstoffverbände (Foam)"],
    "Schaumverband": ["Schaumstoffverbände (Foam)"],
    "PU-Schaumverband": ["Schaumstoffverbände (Foam)"],
    "dünner PU-Schaumverband": ["Schaumstoffverbände (Foam)"],
    "atraumatische Schaumverbände": ["Schaumstoffverbände (Foam)"],
    "saugfähiger Schaumverband": ["Schaumstoffverbände (Foam)"],
    "atraumatischer Schaumverband": ["Schaumstoffverbände (Foam)"],
    "absorbierender Schaumverband": ["Schaumstoffverbände (Foam)"],
    "Superabsorber": ["Superabsorber"],
    "Superabsorber-Verband": ["Superabsorber"],
    "stark saugfähige Superabsorber": ["Superabsorber"],
    "Superabsorber bei stärkerer Sekretion": ["Superabsorber"],
    "Fixiervlies / -pflaster": ["Fixiervlies / -pflaster"],
    "Elastische Fixierbinden": ["Elastische Fixierbinden"],
    "Fixierbinden / kohäsive Binden": ["Fixierbinden / kohäsive Binden"],
    "Nicht erforderlich (selbsthaftender Primärverband)": ["Kein Sekundärverband erforderlich"],

    # Kombinationsverbände (ohne künstliches Fixiervlies)
    "saugfähiger Schaumverband, atraumatische Fixierung": ["Schaumstoffverbände (Foam)"],
    "absorbierender Schaumverband, atraumatische Fixierung": ["Schaumstoffverbände (Foam)"],
    "atraumatische Schaumverbände, ggf. Unterdrucktherapie (VAC) nach Débridement": ["Schaumstoffverbände (Foam)"],
    "PU-Schaumverband, Atraumatische Fixierung": ["Schaumstoffverbände (Foam)"],
    "weicher PU-Schaumverband, weicher PU-Schaumverband": ["Schaumstoffverbände (Foam)"],
    "Elastische Fixierbinden, dünner PU-Schaumverband": ["Schaumstoffverbände (Foam)", "Elastische Fixierbinden"],

    # → Superabsorber, Schaumstoffverbände
    "Superabsorber, hochabsorbierender PU-Schaumverband": ["Superabsorber", "Schaumstoffverbände (Foam)"],
    "Superabsorber oder PU-Schaumverband": ["Superabsorber", "Schaumstoffverbände (Foam)"],
    "Superabsorber weicher PU-Schaumverband": ["Superabsorber", "Schaumstoffverbände (Foam)"],
    "Superabsorber, hochabsorbierende Schaumverbände": ["Superabsorber", "Schaumstoffverbände (Foam)"],
    "PU-Schaumverband oder Superabsorber": ["Superabsorber", "Schaumstoffverbände (Foam)"],

    # → Schaumstoffverbände mit Option auf Superabsorber
    "absorbierender Schaumverband, Superabsorber bei stärkerer Sekretion": ["Schaumstoffverbände (Foam)", "Superabsorber"],
    "weicher PU-Schaumverband Superabsorber bei stärkerem Exsudat": ["Schaumstoffverbände (Foam)", "Superabsorber"],
    "PU-Schaumverband oder Superabsorber bei stärkerer Exsudation": ["Schaumstoffverbände (Foam)", "Superabsorber"],
    "PU-Schaumverband, bei stärkerem Exsudat: Superabsorber": ["Schaumstoffverbände (Foam)", "Superabsorber"],
    "PU-Schaumverband oder kleiner Superabsorber bei stärkerer Sekretion": ["Schaumstoffverbände (Foam)", "Superabsorber"],
    "PU-Schaumverband, Superabsorber bei stärkerer Sekretion": ["Schaumstoffverbände (Foam)", "Superabsorber"],
    "kleiner PU-Schaumverband oder weicher Superabsorber bei stärkerer Exsudation": ["Schaumstoffverbände (Foam)", "Superabsorber"],
    "Superabsorber ergänzen": ["Superabsorber"],

    # → Schaumstoffverbände, sterile Polsterung / Saugkompressen
    "Sterile Saugkompressen / Polsterung": ["Sterile Saugkompressen / Polsterung"],
    "weicher PU-Schaumverband,absorbierende sterile Sekundärauflagen": ["Schaumstoffverbände (Foam)", "Sterile Saugkompressen / Polsterung"],
    "silikonisierter Schaumverband, absorbierende sterile Auflagen": ["Schaumstoffverbände (Foam)", "Sterile Saugkompressen / Polsterung"],
    "weicher absorbierender Schaumverband sterile Saugkompressen": ["Schaumstoffverbände (Foam)", "Sterile Saugkompressen / Polsterung"],
    "weicher PU-Schaumverband, sterile Polsterung": ["Schaumstoffverbände (Foam)", "Sterile Saugkompressen / Polsterung"],
    "silikonisierter Schaumverband, absorbierender PU-Schaumverband": ["Schaumstoffverbände (Foam)"],
    "weicher PU-Schaumverband, druckentlastende Polsterung": ["Schaumstoffverbände (Foam)"],
    "weicher PU-Schaumverband druckreduzierende Polsterung": ["Schaumstoffverbände (Foam)"],
    "weicher PU-Schaumverband, druckreduzierende Polsterung, ggf. Superabsorber": ["Schaumstoffverbände (Foam)", "Superabsorber"],

    # → Kompressionstherapie & Druckentlastung
    "Sekundär: Superabsorber + Fixier-/Kompressionssystem": ["Superabsorber"],
    "abhängig von der Kompressionstherapie": ["abhängig von Kompressionstherapie"],
    "abhängig von Kompressionstherapie": ["abhängig von Kompressionstherapie"],
    "über Kompression": ["abhängig von Kompressionstherapie"],
    "Kompressionstherapie": ["abhängig von Kompressionstherapie"],
    "kommt auf die Kompression an": ["abhängig von Kompressionstherapie"],
    "abhängig von Druckentlastung": ["abhängig von Druckentlastung"],
    "abhängig von der Druckentlastung": ["abhängig von Druckentlastung"],
}

PRODUKT_GT_MAPPING = {
    # Schema-Standardwerte & Schreibweisen
    "Schaumstoffverbände (Foam)": ["Schaumstoffverbände (Foam)"],
    "Schaumstoffverbände": ["Schaumstoffverbände (Foam)"],
    "Hydrofaser / Hydrofiber": ["Hydrofaser / Hydrofiber"],
    "Alginate": ["Alginate"],
    "Hydrogele (Kompresse)": ["Hydrogele (Kompresse)"],
    "Hydrokolloide": ["Hydrokolloide"],
    "Superabsorber": ["Superabsorber"],
    "Wundkontaktschichten (Silikon/Paraffin)": ["Wundkontaktschichten (Silikon/Paraffin)"],

    # Silber entfernt → Basisklasse (gemäß Evaluierungsregel)
    "Silberhydrofaser": ["Hydrofaser / Hydrofiber"],
    "Silberalginat": ["Alginate"],
    "Silber-Schaumverbände": ["Schaumstoffverbände (Foam)"],
    "antimikrobielle Alginate": ["Alginate"],
    "Hydrofaser / Hydrofiber, silberhaltige Varianten bei bakterieller Belastung": ["Hydrofaser / Hydrofiber"],
    "Hydrofaser / Hydrofiber, Wundkontaktschichten (Silikon/Paraffin), Bei bakterieller Belastung: silberhaltige Varianten kurzfristig": ["Hydrofaser / Hydrofiber", "Wundkontaktschichten (Silikon/Paraffin)"],
    "Alginate, Hydrofaser / Hydrofiber, bei kritischer Kolonisation silberhaltige Varianten erwägen": ["Hydrofaser / Hydrofiber", "Alginate"],
    "Hydrofaser / Hydrofiber, Schaumstoffverbände (Foam), Silber-Schaumverbände": ["Hydrofaser / Hydrofiber", "Schaumstoffverbände (Foam)"],
    "Hydrofaser / Hydrofiber, Bei Infektionsverdacht silberhaltige Varianten, Schaumstoffverbände (Foam)": ["Hydrofaser / Hydrofiber", "Schaumstoffverbände (Foam)"],
    "Schaumstoffverbände (Foam), silberhaltige Verbrennungsauflagen": ["Schaumstoffverbände (Foam)"],
    "antiseptische Wundauflagen --> Silber PHMB-haltige Produkte": ["PHMB-haltige Wundauflagen"],

    "Silberhydrofaser oder Silberalginat": ["Hydrofaser / Hydrofiber", "Alginate"],
    "Silberalginate, Silberhydrofaser": ["Hydrofaser / Hydrofiber", "Alginate"],
    "Silberhydrofaser, Silberalginat": ["Hydrofaser / Hydrofiber", "Alginate"],
    "Silberhydrofaser, antimikrobielle Alginate": ["Hydrofaser / Hydrofiber", "Alginate"],
    "silberhydrofaser/Silberalginat bei kritischer Kolonisation": ["Hydrofaser / Hydrofiber", "Alginate"],
    "Silberalginat, antimikrobielle Alginate ggf. PHMB-haltige Wundauflagen": ["Alginate", "PHMB-haltige Wundauflagen"],
    "Bei feuchten/infizierten Bereichen: Silberhydrofaser Silberalginat antimikrobielle Wundauflagen.": ["Hydrofaser / Hydrofiber", "Alginate"],
    "Bei feuchten/infizierten Bereichen: Silberhydrofaser Silberalginat antimikrobielle Wundauflagen": ["Hydrofaser / Hydrofiber", "Alginate"],
    "Bei kritischer Kolonisation: Silberhydrofaser kurzfristig, Hydrogele (Kompresse)": ["Hydrofaser / Hydrofiber", "Hydrogele (Kompresse)"],
    "Bei kritischer Kolonisation: Silberhydrofaser kurzfristig": ["Hydrofaser / Hydrofiber"],
    "Alginate bei stärker exsudierend": ["Alginate"],
    "ggf. Hydrogel bei trockeneren Belägen": ["Hydrogele (Kompresse)"],
    "Alginate, Hydrofaser / Hydrofiber, Superabsorber, ggf. Unterdrucktherapie (NPWT/VAC) nach Nekrosensanierung": ["Alginate", "Hydrofaser / Hydrofiber", "Superabsorber"],

    # PHMB
    "PHMB-haltige Auflagen": ["PHMB-haltige Wundauflagen"],
    "PHMB-haltige Wundauflagen": ["PHMB-haltige Wundauflagen"],
    "antimikrobielle Alginate ggf. PHMB-haltige Wundauflagen": ["Alginate", "PHMB-haltige Wundauflagen"],

    # Trockene-Nekrose-Schutzverbände normalisiert
    "trockene sterile Schutzverbände, atraumatische Kontaktlagen, keine aggressive Befeuchtung der stabilen Nekrose": ["trockene sterile Schutzverbände", "Wundkontaktschichten (Silikon/Paraffin)"],
    "Bei trockener Nekrose: trockener Schutzverband atraumatische Kontaktlagen.": ["trockene sterile Schutzverbände", "Wundkontaktschichten (Silikon/Paraffin)"],
    "Bei trockenen Nekrosen: atraumatische trockene Schutzverbände": ["trockene sterile Schutzverbände"],
    "trockene sterile Abdeckung, atraumatische Schutzverbände, keine aggressive Befeuchtung": ["trockene sterile Schutzverbände"],
    "Bei trockenen Nekrosen: atraumatische trockene Schutzverbände, Bei feuchten/infizierten Bereichen: Silberhydrofaser Silberalginat antimikrobielle Wundauflagen": ["trockene sterile Schutzverbände", "Hydrofaser / Hydrofiber", "Alginate"],

    # Wundtyp-abhängig → Produkte behalten
    "Hydrogel bei trockenen Nekroseanteilen, Hydrofaser oder Alginat bei Exsudat": ["Hydrogele (Kompresse)", "Hydrofaser / Hydrofiber", "Alginate"],
}

DEBRIDEMENT_GT_MAPPING = {
    # Schema-Standardwerte (Katalog)
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)"],
    "Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)": ["Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "Chirurgisch/Scharf (Skalpell, Kürette)": ["Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Enzymatisch (Kollagenase)": ["Enzymatisch (Kollagenase)"],
    "Kein Débridement erforderlich": ["Kein Débridement erforderlich"],

    # Äquivalente Phrasen & Kombinationen
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), vorsichtige mechanische Reinigung lockerer Beläge": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), vorsichtig mechanisches Debridement": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "vorsichtig mechanisches Debridement": ["Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "vorsichtige mechanische Reinigung lockerer Beläge": ["Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "nicht aggressiv entfernen, solange keine Revaskularisation erfolgt ist, Chirurgisch/Scharf (Skalpell, Kürette)": ["Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), chirurgisches Debridement erst nach Perfusionsverbesserung, sofern möglich": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Chirurgisch/Scharf (Skalpell, Kürette)"],
    "chirurgisches Debridement erst nach Perfusionsverbesserung, sofern möglich": ["Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Chirurgisch/Scharf (Skalpell, Kürette), autolytisches Debridement, enzymatisches Debridement - ergänzend": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Chirurgisch/Scharf (Skalpell, Kürette)", "Enzymatisch (Kollagenase)"],
    "autolytisches Debridement, enzymatisches Debridement - ergänzend": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Enzymatisch (Kollagenase)"],
    "konservatives Abwarten bei unklarer Demarkation, selektives chirurgisches Débridement, enzymatisch/autolytisch ergänzend": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Chirurgisch/Scharf (Skalpell, Kürette)", "Enzymatisch (Kollagenase)"],
    "kein aggressives Debridement ohne Gefäßstatus, trockene stabile Nekrosen ggf. belassen, Bei infizierten/fibrinösen Belägen: zurückhaltendes scharfes Debridement, autolytische Verfahren möglich": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Chirurgisch/Scharf (Skalpell, Kürette)"],

    "Autolytisch (Hydrogele, Folienverbände), Hydrokolloide": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)"],
    "Autolytisch (Hydrogele, Folienverbände), Hydrokolloide, Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "Autolytisch (Hydrogele, Chirurgisch/Scharf (Skalpell, Folienverbände), Hydrokolloide, Kürette), Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)", "Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Chirurgisch/Scharf (Skalpell, Kürette), Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen": ["Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)", "Chirurgisch/Scharf (Skalpell, Kürette)"],
    "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände), Chirurgisch/Scharf (Skalpell, Kürette), Enzymatisch": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Chirurgisch/Scharf (Skalpell, Kürette)", "Enzymatisch (Kollagenase)"],
    "Mechanisch (Monofilament-Pad, Wundspülung), feuchte Kompressen": ["Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"],
    "Autolytisch (Hydrogele, Chirurgisch/Scharf (Skalpell, Folienverbände), Hydrokolloide, Kürette)": ["Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)", "Chirurgisch/Scharf (Skalpell, Kürette)"],
}

SPUELLOESUNG_GT_MAPPING = {
    # Schema-Standardwerte & Katalog-Strings
    "Neutrale Spüllösung (NaCl 0,9 % / Ringer-Lösung)": ["Neutrale Spüllösung (NaCl 0,9 % / Ringer-Lösung)"],
    "Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)": ["Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)"],
    "Neutrale Spüllösung (NaCl, Ringer)": ["Neutrale Spüllösung (NaCl 0,9 % / Ringer-Lösung)"],
    "Antimikrobielle Spüllösung (PHMB, Octenisept)": ["Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)"],

    # Synonyme & Phrasen
    "PHMB oder Octenidin zeitlich begrenzt": ["Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)"],
    "Bei kritischer Kolonisation: PHMB oder Octenidin zeitlich begrenzt": ["Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)"],
    "bei kritischer Kolonisation: PHMB oder Octenidin zeitlich begrenzt": ["Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)"],
    "bei kritischer Kolonisation: PHMB/Octenidin": ["Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)"],
    "bei kritischer Kolonisation: mit PHMB/Octenidin": ["Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)"],
    "Antiseptika nur gezielt bei: Infektionszeichen, kritischer Kolonisation": ["Antimikrobielle Spüllösung (PHMB / Octenidin / Hypochlorit)"],
}

ANTIMIKROBIELL_GT_MAPPING = {
    # Schema-Standardwerte & Schreibweisen
    "Silber (Ag⁺)": ["Silber (Ag+)"],
    "Silber (Ag+)": ["Silber (Ag+)"],
    "PHMB": ["PHMB"],
    "Octenidin": ["Octenidin"],
    "Cadexomer-Iod": ["Cadexomer-Iod"],
    "Honig (Medihoney)": ["Honig (Medihoney)"],
}

HAUTSCHUTZ_GT_MAPPING = {
    # Schema-Standardwerte
    "Hautschutzfilm / Barrierespray": ["Hautschutzfilm / Barrierespray"],
    "Zinksalbe / Zinkpaste": ["Zinksalbe / Zinkpaste"],
    "Wundrandschutzpaste": ["Wundrandschutzpaste"],
    "Nicht erforderlich": ["Kein Hautschutz erforderlich"],
}

KOMPRESSION_GT_MAPPING = {
    # Schema-Standardwerte
    "Mehrkomponentensysteme (2-/4-Lagen)": ["Mehrkomponentensysteme (2-/4-Lagen)"],
    "Kurzzugbinden": ["Kurzzugbinden"],
    "Adaptive Kompressionsbandagen (Wrap)": ["Adaptive Kompressionsbandagen (Wrap)"],
    "Medizinische Kompressionsstrümpfe (MKS)": ["Medizinische Kompressionsstrümpfe (MKS)"],
    "medizinische Kompressionssysteme": ["Medizinische Kompressionsstrümpfe (MKS)"],
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
                    "gluteal", "intergluteal", "leiste", "leistenregion", "inguinal"],
}

