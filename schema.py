SCHEMA_VERSION = "1.4"

import copy

# Umgang mit "Sonstiges"-Optionen:
#
# STRING-Felder (enum):
#   - wundtyp = "Sonstiges"  →  wundtyp_sonstiges muss befüllt sein (z.B. "Pyoderma gangraenosum")
#
# ARRAY-Felder:
#   "Sonstiges" wurde aus allen Enums entfernt. Das LLM trägt stattdessen den
#   konkreten Freitext direkt als String ins Array ein, z.B.:
#       "wundrand": ["Mazeriert", "Livide Verfärbung"]
#   Die Enum-Werte in den descriptions dienen nur als Vorschlagsliste.
#
# Änderungen v1.4:
#   - praeferenz_verbandklasse wieder als flaches Array (einzelnes Behandlungsset aus 1+ Verbandklassen)
#   - alternativ_verbandklasse wieder hinzugefügt (einzelnes alternatives Behandlungsset oder null)

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {

        # --- Kategorie 1: Wundsituation ---

        "wundtyp": {
            "type": "string",
            "enum": [
                "Dekubitus",
                "Ulkus cruris venosum",
                "Ulkus cruris arteriosum",
                "Ulkus cruris mixtum",
                "Diabetisches Fußulkus",
                "Traumatische Wunde",
                "Tumorwunde",
                "Verbrennungswunde",
                "Postoperative Wunde",
                "Sonstiges"
            ],
            "description": "Wundtyp. Bei 'Sonstiges' muss wundtyp_sonstiges befüllt sein."
        },
        "wundtyp_sonstiges": {
            "type": "string",
            "description": (
                "Konkreter Wundtyp wenn wundtyp = 'Sonstiges', z.B. 'Pyoderma gangraenosum'. "
                "Leer lassen wenn wundtyp != 'Sonstiges'."
            )
        },
        "wundtyp_spezifizierung": {
            "type": "string",
            "description": "Optionale Spezifizierung: Gradangabe, Subtyp, Ergänzung. Leer lassen wenn nicht vorhanden."
        },
        "lokalisation": {
            "type": "string",
            "description": "Körperregion und Seitenangabe, z.B. 'Unterschenkel rechts lateral', 'Sakralregion'"
        },
        "wundphase": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Wundphase(n), Mehrfachauswahl möglich. "
                "Vorschlagswerte: 'Nekrose / Eschara', 'Fibrinbelag / Slough', 'Granulation', "
                "'Epithelisierung', 'Gemischt'. "
                "Falls keiner passt: konkreten Freitext direkt als String eintragen."
            )
        },
        "exsudat_menge": {
            "type": "string",
            "enum": ["Keine", "Leicht", "Mäßig", "Stark", "Sehr stark"],
            "description": "Exsudatmenge"
        },
        "infektionsstatus": {
            "type": "string",
            "enum": [
                "Keine Infektionszeichen",
                "Verdacht auf Infektion / kritische Kolonisation",
                "Deutliche Infektionszeichen"
            ],
            "description": "Infektionsstatus"
        },
        "wundrand": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Beschaffenheit des Wundrands, Mehrfachauswahl möglich. "
                "Vorschlagswerte: 'Reizlos / unauffällig', 'Mazeriert', 'Hyperkeratotisch', "
                "'Unterminiert (Wundtaschen)', 'Epibolie (eingerollter Wundrand)', 'Gerötet / entzündlich'. "
                "Falls keiner passt: konkreten Freitext direkt als String eintragen, z.B. 'Sklerotisch'."
            )
        },
        "wundumgebung": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Zustand der Wundumgebung, Mehrfachauswahl möglich. "
                "Vorschlagswerte: 'Reizlos / intakt', 'Erythem / Rötung', 'Mazeration', 'Ödem', "
                "'Ekzem / Dermatitis', 'CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)'. "
                "Falls keiner passt: konkreten Freitext direkt als String eintragen."
            )
        },
        "weitere_auffaelligkeiten": {
            "type": "string",
            "description": "Weitere Auffälligkeiten: Geruch, Schmerzen, Besonderheiten. Leer lassen wenn keine."
        },

        # --- Kategorie 2: Wundreinigung / Débridement ---

        "debridement_notwendig": {
            "type": "string",
            "enum": ["ja", "nein"],
            "description": "Ist eine Wundreinigung / Débridement notwendig?"
        },
        "spuelloesung": {
            "type": "string",
            "enum": [
                "Neutrale Spüllösung (NaCl, Ringer)",
                "Antimikrobielle Spüllösung (PHMB, Octenisept)",
                ""
            ],
            "description": "Empfohlene Spüllösung. Leer lassen wenn nicht indiziert."
        },
        "debridement_methode": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Débridement-Methode(n), Mehrfachauswahl möglich. "
                "Wähle die passende(n) Methode(n) als exakte(n) String(s) aus dem bereitgestellten Wundversorgungs-Katalog (<product_catalog>) aus. "
                "Nutze exakt die Schreibweise aus dem Katalog. Falls keine passt: konkreten Freitext direkt als String eintragen."
            )
        },

        # --- Kategorie 3: Primärverband ---

        "praeferenz_verbandklasse": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "description": (
                    "Präferenzierte primäre Wundauflage, basierend auf dem Wundbild. "
                    "Empfehle ein Behandlungsset aus verschiedenen Verbandsklassen. Diese Klassen werden dann als Set gemeinsam angewendet. "
                    "Wähle nur so viele Verbandsklassen aus wie für das Behandlungsset nötig sind. "
                    "WICHTIG – diese Felder NICHT hier eintragen (sie haben eigene Felder im Schema): "
                    "Antimikrobielle Agenzien (Silber, PHMB, Manuka etc.) → 'antimikrobielles_agens' "
                    "Sekundärverband / Fixierung (Fixiervlies, Binden) → 'sekundaerverband_fixierung' "
                    "Hautschutz (Barrierespray, Zinksalbe) → 'wundrand_hautschutz'. "
                    "Wähle die passende(n) Klasse(n) als exakte(n) String(s) aus den im bereitgestellten Wundversorgungs-Katalog (<product_catalog>) unter 'Primärverbände' aufgelisteten Optionen. "
                    "Nutze exakt die Schreibweise aus dem Katalog. Falls keine passt: konkreten Freitext direkt als String eintragen."
                )
        },
        "alternativ_verbandklasse": {
            "type": ["array", "null"],
            "items": {"type": "string"},
            "minItems": 1,
            "description": (
                "Alternatives Behandlungsset für die primäre Wundauflage. Referenz: das bereits gewählte Präferenzset. "
                "Nur befüllen wenn therapeutisch gleichwertig UND mindestes eine Verbandklasse unterscheidet sich vom Präferenzset. Sonst: null. "
                "WICHTIG – diese Felder NICHT hier eintragen (sie haben eigene Felder im Schema): "
                "Antimikrobielle Agenzien (Silber, PHMB, Manuka etc.) → 'antimikrobielles_agens' "
                "Sekundärverband / Fixierung (Fixiervlies, Binden) → 'sekundaerverband_fixierung' "
                "Hautschutz (Barrierespray, Zinksalbe) → 'wundrand_hautschutz'. "
                "Wähle die passende(n) Klasse(n) als exakte(n) String(s) aus den im bereitgestellten Wundversorgungs-Katalog (<product_catalog>) unter 'Primärverbände' aufgelisteten Optionen. "
                "Nutze exakt die Schreibweise aus dem Katalog. Falls keine passt: konkreten Freitext direkt als String eintragen."
            )
        },
        "antimikrobieller_verband": {
            "type": "string",
            "enum": ["ja", "nein"],
            "description": "Soll der Primärverband antimikrobiell sein?"
        },
        "antimikrobielles_agens": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Antimikrobielles Agens, nur wenn antimikrobieller_verband = 'ja'. "
                "Wähle die passende(n) Option(en) als exakte(n) String(s) aus den im bereitgestellten Wundversorgungs-Katalog (<product_catalog>) unter 'Antimikrobielle Verbände' aufgelisteten Optionen. "
                "Nutze exakt die Schreibweise aus dem Katalog. Falls keine passt: konkreten Freitext direkt als String eintragen. "
                "Leeres Array wenn antimikrobieller_verband = 'nein'."
            )
        },

        # --- Kategorie 4: Sekundärverband / Fixierung / Hautschutz ---

        "sekundaerverband_fixierung": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Sekundärverband / Fixierung. Mehrfachauswahl möglich. "
                "Wähle die passende(n) Option(en) als exakte(n) String(s) aus den im bereitgestellten Wundversorgungs-Katalog (<product_catalog>) unter 'Sekundärverband / Fixierung' aufgelisteten Optionen. "
                "Nutze exakt die Schreibweise aus dem Katalog. Falls keine passt: konkreten Freitext direkt als String eintragen."
            )
        },
        "wundrand_hautschutz": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Wundrand- / Hautschutz. Mehrfachauswahl möglich. "
                "Wähle die passende(n) Option(en) als exakte(n) String(s) aus den im bereitgestellten Wundversorgungs-Katalog (<product_catalog>) unter 'Wundrand- / Hautschutz' aufgelisteten Optionen. "
                "Nutze exakt die Schreibweise aus dem Katalog. Falls keine passt: konkreten Freitext direkt als String eintragen."
            )
        },

        # --- Kategorie 5: Kompressionstherapie ---

        "kompression_indiziert": {
            "type": "string",
            "enum": ["ja", "nein", "nicht beurteilbar"],
            "description": "Ist eine Kompressionstherapie indiziert?"
        },
        "kompression_art": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "Art der Kompression, nur wenn kompression_indiziert = 'ja'. Mehrfachauswahl möglich. "
                "Wähle die passende(n) Option(en) als exakte(n) String(s) aus den im bereitgestellten Wundversorgungs-Katalog (<product_catalog>) unter 'Kompressionstherapie' aufgelisteten Optionen. "
                "Nutze exakt die Schreibweise aus dem Katalog. Falls keine passt: konkreten Freitext direkt als String eintragen. "
                "Leeres Array wenn kompression_indiziert != 'ja'."
            )
        },

        # --- Kategorie 6: Einschränkungen & Annahmen ---

        "einschraenkungen_annahmen": {
            "type": "string",
            "description": "Fehlende Informationen, getroffene Annahmen. Leer lassen wenn keine."
        },
    },

    "required": [
        "wundtyp",
        "wundtyp_sonstiges",
        "wundtyp_spezifizierung",
        "lokalisation",
        "wundphase",
        "exsudat_menge",
        "infektionsstatus",
        "wundrand",
        "wundumgebung",
        "weitere_auffaelligkeiten",
        "debridement_notwendig",
        "spuelloesung",
        "debridement_methode",
        "praeferenz_verbandklasse",
        "alternativ_verbandklasse",
        "antimikrobieller_verband",
        "antimikrobielles_agens",
        "sekundaerverband_fixierung",
        "wundrand_hautschutz",
        "kompression_indiziert",
        "kompression_art",
        "einschraenkungen_annahmen",
    ]
}


EXAMPLE_OUTPUT = {
    # Normaler Fall: kein Sonstiges nötig
    "wundtyp": "Ulcus cruris venosum",
    "wundtyp_sonstiges": "",
    "wundtyp_spezifizierung": "",
    "lokalisation": "Unterschenkel rechts lateral",
    "wundphase": ["Fibrinbelag / Slough", "Granulation"],
    "exsudat_menge": "Stark",
    "infektionsstatus": "Verdacht auf Infektion / kritische Kolonisation",
    "wundrand": ["Mazeriert", "Gerötet / entzündlich"],
    "wundumgebung": [
        "Erythem / Rötung",
        "Ödem",
        "CVI-typische Hautveränderungen (Hyperpigmentierung, Atrophie blanche, Lipodermatosklerose)"
    ],
    "weitere_auffaelligkeiten": "Leichter Geruch",
    "debridement_notwendig": "ja",
    "spuelloesung": "Antimikrobielle Spüllösung (PHMB, Octenisept)",
    "debridement_methode": [
        "Autolytisch (Hydrogele, Hydrokolloide, Folienverbände)",
        "Mechanisch (Monofilament-Pad, feuchte Kompressen, Wundspülung)"
    ],
    "praeferenz_verbandklasse": ["Hydrofaser / Hydrofiber", "Schaumstoffverbände (Foam)"],
    "alternativ_verbandklasse": ["Alginate", "Schaumstoffverbände (Foam)"],
    "antimikrobieller_verband": "ja",
    "antimikrobielles_agens": ["Silber (Ag+)"],
    "sekundaerverband_fixierung": ["Fixiervlies / -pflaster"],
    "wundrand_hautschutz": ["Hautschutzfilm / Barrierespray"],
    "kompression_indiziert": "ja",
    "kompression_art": ["Mehrkomponentensysteme (2-/4-Lagen)"],
    "einschraenkungen_annahmen": "ABI-Wert nicht dokumentiert, Kompression unter Vorbehalt empfohlen."
}

EXAMPLE_OUTPUT_SONSTIGES = {
    # Sonstiges-Fall: Freitexte konkret befüllt
    "wundtyp": "Sonstiges",
    "wundtyp_sonstiges": "Pyoderma gangraenosum",        # <-- konkret statt leer
    "wundtyp_spezifizierung": "therapierefraktär",
    "lokalisation": "Unterschenkel links medial",
    "wundphase": ["Nekrose / Eschara", "Calcinosis cutis"],  # <-- letzter Wert = Freitext
    "exsudat_menge": "Sehr stark",
    "infektionsstatus": "Deutliche Infektionszeichen",
    "wundrand": ["Unterminiert (Wundtaschen)", "Livide Verfärbung"],  # <-- Freitext
    "wundumgebung": ["Erythem / Rötung", "Bullöse Veränderungen"],   # <-- Freitext
    "weitere_auffaelligkeiten": "Starker Geruch, Schmerzen VAS 8/10",
    "debridement_notwendig": "ja",
    "spuelloesung": "Antimikrobielle Spüllösung (PHMB, Octenisept)",
    "debridement_methode": [
        "Chirurgisch/Scharf (Skalpell, Kürette)",
        "Enzymatisch (Kollagenase)"                                   # <-- Freitext
    ],
    "praeferenz_verbandklasse": ["Superabsorber", "Hydrofaser / Hydrofiber"],
    "alternativ_verbandklasse": ["Schaumstoffverbände (Foam)"],
    "antimikrobieller_verband": "ja",
    "antimikrobielles_agens": ["PHMB", "Cadexomer-Iod"],             # <-- Freitext
    "sekundaerverband_fixierung": ["Elastische Fixierbinden"],
    "wundrand_hautschutz": ["Zinksalbe / Zinkpaste"],
    "kompression_indiziert": "nein",
    "kompression_art": [],
    "einschraenkungen_annahmen": (
        "Grunderkrankung (Pyoderma gangraenosum) erfordert immunsuppressive Systemtherapie; "
        "Wundversorgung allein nicht kurativ."
    )
}

