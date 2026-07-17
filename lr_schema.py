SCHEMA_VERSION = "2.1"

# Änderungen v2.1:
#   - Komplett an das allgemeine Schema (schema.py) angepasst und flach strukturiert.
#   - Deutschsprachige Feldnamen, die den Aufbau von schema.py spiegeln.
#   - Verwendung von praeferenz_wundauflage, alternativ_wundauflage,
#     praeferenz_ergaenzung, alternativ_ergaenzung und kompression_produkt
#     für die L&R-Produktempfehlungen (flache Arrays).

OUTPUT_SCHEMA_LR = {
    "type": "object",
    "properties": {

        # --- Kategorie 1: Wundsituation ---

        "wundtyp": {
            "type": "string",
            "description": "Wundtyp (Freitext), z. B. Dekubitus, Ulcus cruris, diabetisches Fußulkus, postoperative Wunde."
        },
        "lokalisation": {
            "type": "string",
            "description": "Körperregion und Seitenangabe, z.B. 'Unterschenkel rechts lateral', 'Sakralregion'"
        },
        "wundstadium": {
            "type": "string",
            "enum": [
                "Exsudation",
                "Nekrose",
                "Fibrinbelag",
                "Granulation",
                "Epithelisierung",
                "Infektion",
                "Sonstiges"
            ],
            "description": "Wundstadium. Bei 'Sonstiges' muss wundstadium_sonstiges befüllt sein."
        },
        "wundstadium_sonstiges": {
            "type": "string",
            "description": "Konkretes Wundstadium wenn wundstadium = 'Sonstiges'. Leer lassen wenn wundstadium != 'Sonstiges'."
        },
        "wundgrund": {
            "type": "string",
            "description": "Beschreibung des Wundgrunds / sichtbaren Gewebes (Freitext)."
        },
        "wundrand": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "Reizlos / unauffällig",
                    "Mazeriert",
                    "Hyperkeratotisch",
                    "Unterminiert (Wundtaschen)",
                    "Epibolie (eingerollter Wundrand)",
                    "Gerötet / entzündlich",
                    "Sonstiges"
                ]
            },
            "description": "Beschaffenheit des Wundrands, Mehrfachauswahl möglich. Bei 'Sonstiges' muss wundrand_sonstiges befüllt sein."
        },
        "wundrand_sonstiges": {
            "type": "string",
            "description": "Konkrete Beschaffenheit des Wundrands wenn wundrand 'Sonstiges' enthält. Leer lassen wenn wundrand kein 'Sonstiges' enthält."
        },
        "wundumgebung": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "Reizlos / intakt",
                    "Erythem / Rötung",
                    "Mazeration",
                    "Ödem",
                    "Ekzem / Dermatitis",
                    "CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)",
                    "Sonstiges"
                ]
            },
            "description": "Zustand der Wundumgebung, Mehrfachauswahl möglich. Bei 'Sonstiges' muss wundumgebung_sonstiges befüllt sein."
        },
        "wundumgebung_sonstiges": {
            "type": "string",
            "description": "Konkreter Zustand der Wundumgebung wenn wundumgebung 'Sonstiges' enthält. Leer lassen wenn wundumgebung kein 'Sonstiges' enthält."
        },
        "exsudat_menge": {
            "type": "string",
            "enum": ["Keine", "Leicht", "Mäßig", "Stark", "Sehr stark"],
            "description": "Exsudatmenge"
        },
        "weitere_auffaelligkeiten": {
            "type": "string",
            "description": "Weitere Auffälligkeiten oder Besonderheiten: Geruch, Schmerzen, Besonderheiten. Leer lassen wenn keine."
        },

        # --- Kategorie 2: Wundbettvorbereitung / Débridement ---

        "debridement_notwendig": {
            "type": "string",
            "enum": ["ja", "nein"],
            "description": "Ist eine Wundbettvorbereitung / Débridement notwendig?"
        },
        "debridement_methode": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Wundbettvorbereitung / Débridement-Methode aus dem L&R-Produktkatalog (lr0). "
                "Mehrfachauswahl möglich."
            )
        },

        # --- Kategorie 3: Infektion & Spüllösung ---

        "infektion_vorhanden": {
            "type": "string",
            "enum": ["ja", "nein"],
            "description": "Besteht eine Infektion der Wunde?"
        },
        "spuelloesung": {
            "type": "string",
            "enum": [
                "Neutrale Spüllösung",
                "Antimikrobielle Spüllösung",
                ""
            ],
            "description": "Empfohlene Spüllösung, nur wenn infektion_vorhanden = 'ja'. Leer lassen wenn nicht indiziert."
        },

        # --- Kategorie 4: Wundauflagen (Primärwundauflagen) ---

        "praeferenz_wundauflage": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "description": (
                "Präferierte Wundauflage (Primärwundauflage) aus dem L&R-Produktkatalog (lr1). "
                "Empfehle ein Behandlungsset aus verschiedenen Produkten, die gemeinsam angewendet werden."
            )
        },
        "alternativ_wundauflage": {
            "type": ["array", "null"],
            "items": {"type": "string"},
            "minItems": 1,
            "description": (
                "Alternative Wundauflage (Primärwundauflage) aus dem L&R-Produktkatalog (lr1). "
                "Nur befüllen, wenn therapeutisch gleichwertig und mindestens ein Produkt sich unterscheidet, sonst null."
            )
        },

        # --- Kategorie 5: Ergänzende Produkte (Sekundärwundauflagen) ---

        "praeferenz_ergaenzung": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Präferierte ergänzende Produkte / Sekundärwundauflagen (z. B. Fixierung, Binden, Pflaster) "
                "aus den L&R-Produktkatalogen (lr2_produktkatalog und lr3_produktkatalog). WICHTIG: Entscheide zuerst, "
                "ob ein Sekundärverband / ergänzendes Produkt notwendig ist. Wenn nicht notwendig, gib ein leeres Array [] an. Mehrfachauswahl möglich."
            )
        },
        "alternativ_ergaenzung": {
            "type": ["array", "null"],
            "items": {"type": "string"},
            "description": (
                "Alternative ergänzende Produkte / Sekundärwundauflagen aus den L&R-Produktkatalogen (lr2_produktkatalog und lr3_produktkatalog). "
                "Nur befüllen, wenn praeferenz_ergaenzung nicht leer ist und mindestens ein Produkt sich unterscheidet, sonst null oder leeres Array []."
            )
        },

        # --- Kategorie 6: Kompressionstherapie ---

        "kompression_indiziert": {
            "type": "string",
            "enum": ["ja", "nein"],
            "description": "Ist eine Kompressionstherapie indiziert?"
        },
        "kompression_produkt": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Kompressionstherapie-Produkte aus dem L&R-Produktkatalog (lr3). "
                "Mehrfachauswahl möglich. Nur befüllen, wenn kompression_indiziert = 'ja', sonst leeres Array."
            )
        },

        # --- Kategorie 7: Einschränkungen & Annahmen ---

        "einschraenkungen_annahmen": {
            "type": "string",
            "description": "Fehlende Informationen, getroffene Annahmen. Leer lassen wenn keine."
        },
    },

    "required": [
        "wundtyp",
        "lokalisation",
        "wundstadium",
        "wundstadium_sonstiges",
        "wundgrund",
        "wundrand",
        "wundrand_sonstiges",
        "wundumgebung",
        "wundumgebung_sonstiges",
        "exsudat_menge",
        "weitere_auffaelligkeiten",
        "debridement_notwendig",
        "debridement_methode",
        "infektion_vorhanden",
        "spuelloesung",
        "praeferenz_wundauflage",
        "alternativ_wundauflage",
        "praeferenz_ergaenzung",
        "alternativ_ergaenzung",
        "kompression_indiziert",
        "kompression_produkt",
        "einschraenkungen_annahmen",
    ]
}


EXAMPLE_OUTPUT_LR = {
    "wundtyp": "Ulcus cruris venosum",
    "lokalisation": "Unterschenkel rechts lateral",
    "wundstadium": "Granulation",
    "wundstadium_sonstiges": "",
    "wundgrund": "Fibrinbelag / Slough, Granulationsgewebe",
    "wundrand": ["Mazeriert"],
    "wundrand_sonstiges": "",
    "wundumgebung": ["Ödem"],
    "wundumgebung_sonstiges": "",
    "exsudat_menge": "Mäßig",
    "weitere_auffaelligkeiten": "Leichter Geruch",
    "debridement_notwendig": "ja",
    "debridement_methode": ["Debrisoft Pad"],
    "infektion_vorhanden": "nein",
    "spuelloesung": "",
    "praeferenz_wundauflage": ["Suprasorb Liquacel Pro", "Suprasorb P Sensitive"],
    "alternativ_wundauflage": ["Suprasorb A Pro", "Suprasorb P Sensitive"],
    "praeferenz_ergaenzung": ["Curafix H"],
    "alternativ_ergaenzung": ["Curapor"],
    "kompression_indiziert": "ja",
    "kompression_produkt": ["Rosidal sys"],
    "einschraenkungen_annahmen": "ABI-Wert nicht dokumentiert, Kompression unter Vorbehalt empfohlen."
}


EXAMPLE_OUTPUT_LR_SONSTIGES = {
    "wundtyp": "Pyoderma gangraenosum, therapierefraktär",
    "lokalisation": "Unterschenkel links medial",
    "wundstadium": "Sonstiges",
    "wundstadium_sonstiges": "Nekrosestadium mit Calcinosis cutis",
    "wundgrund": "Nekrose / Eschara, Calcinosis cutis",
    "wundrand": ["Sonstiges"],
    "wundrand_sonstiges": "Extrem schmerzhaft gerötet",
    "wundumgebung": ["Sonstiges"],
    "wundumgebung_sonstiges": "Milde Schuppung",
    "exsudat_menge": "Sehr stark",
    "weitere_auffaelligkeiten": "Starker Geruch, Schmerzen VAS 8/10",
    "debridement_notwendig": "ja",
    "debridement_methode": ["Chirurgisches Debridement", "Autolytisches Debridement"],
    "infektion_vorhanden": "ja",
    "spuelloesung": "Antimikrobielle Spüllösung",
    "praeferenz_wundauflage": ["Vliwasorb Pro", "Suprasorb Liquacel Pro"],
    "alternativ_wundauflage": ["Suprasorb P Sensitive"],
    "praeferenz_ergaenzung": ["Mollelast"],
    "alternativ_ergaenzung": ["Curafix H"],
    "kompression_indiziert": "nein",
    "kompression_produkt": [],
    "einschraenkungen_annahmen": "Grunderkrankung (Pyoderma gangraenosum) erfordert immunsuppressive Systemtherapie; Wundversorgung allein nicht kurativ."
}