"""
Lokalisation Mapping Dictionary (Wundlokalisation)

Dieses Modul definiert die Regeln und Funktionen für das saubere 1:1 Mapping von 
Freitexten und Rohangaben zur anatomischen Lokalisation (Experten & KI-Ansätze)
auf das einheitliche 6-Klassen-Schema:

1. Fuß (inkl. Fersendekubitus, Zehen, Malleolus, plantar, Vorfuß, Mittfuß, linker/rechter Fuß)
2. Bein (inkl. Unterschenkel, Oberschenkel, Knie, Wade, Untere Extremität)
3. Gesäß / Sakral (inkl. Sacrum, Sacralbereich, Sakralregion, Steiß, Interglutealfalte)
4. Arm / Hand (inkl. Oberarm, Unterarm, Handrücken, Ellenbeuge, Finger, Obere Extremität)
5. Abdomen (inkl. Bauchdecke, Peristomal, Stomabereich, Unterbauch)
6. Enthaltung / keine Angabe (nur wenn gar kein Körperteil genannt oder beurteilt wird)
"""

EXPLICIT_LOKALISATION_RULES = {
    "Fuß": "Fuß",
    "Bein": "Bein",
    "Gesäß": "Gesäß / Sakral",
    "Gesäß/Steiß": "Gesäß / Sakral",
    "Abdomen": "Abdomen",
    "Arm": "Arm / Hand",
    "Hand": "Arm / Hand",
    "Arm, Hand": "Arm / Hand",
    "Bein, Fuß": "Fuß",
    "?": "Enthaltung / keine Angabe",
    "???": "Enthaltung / keine Angabe",
    "keine Angabe möglich": "Enthaltung / keine Angabe",
    "nicht beurteilbar": "Enthaltung / keine Angabe",
    "nicht genau definierbar": "Enthaltung / keine Angabe",
    "lokalisation nicht genau zu definieren": "Enthaltung / keine Angabe"
}

def map_lokalisation_explicit(val_str):
    """
    Mappt eine Roh-Eingabe zur Lokalisation auf die 6 Standard-Kategorien.
    Ignoriert Seiten-Unklarheiten (z.B. "Unterschenkel (Seite unklar)") und mappt
    prioritär auf die genannte Körperregion.
    Returns string (1:1 mapped category).
    """
    if not val_str or str(val_str).strip() in ["keine Angabe", "nan", "?", "???", "keine Angabe möglich", "nicht beurteilbar", "nicht genau definierbar", "lokalisation nicht genau zu definieren", "N/A"]:
        return "Enthaltung / keine Angabe"

    s_clean = str(val_str).strip()
    if s_clean in EXPLICIT_LOKALISATION_RULES:
        return EXPLICIT_LOKALISATION_RULES[s_clean]

    v = s_clean.lower()

    # Priority 1: Body region recognition (ignores side/laterality uncertainty notes!)
    if "abdomen" in v or "bauch" in v or "stoma" in v or "peristoma" in v or "unterbauch" in v:
        return "Abdomen"
    if "gesäß" in v or "sakral" in v or "sacral" in v or "steiß" in v or "sacrum" in v or "glutä" in v or "glutäal" in v or "paraglutäal" in v or "os sacrum" in v or "intergluteal" in v or "sakrokokzygeal" in v:
        return "Gesäß / Sakral"
    if "fuß" in v or "fuss" in v or "fers" in v or "zeh" in v or "plantar" in v or "malleol" in v or "vorfuß" in v or "außenknöchel" in v or "innenknöchel" in v or "mittfuß" in v or "zehe" in v:
        return "Fuß"
    if "bein" in v or "unterschenkel" in v or "oberschenkel" in v or "knie" in v or "femur" in v or "schienbein" in v or "wade" in v or "untere extremität" in v or "untere extremitaet" in v:
        return "Bein"
    if "arm" in v or "hand" in v or "oberarm" in v or "unterarm" in v or "ellenbeug" in v or "finger" in v or "handrücken" in v or "obere extremität" in v or "obere extremitaet" in v:
        return "Arm / Hand"

    # Priority 2: Refusal / Complete inability to assess (ONLY IF NO body part matched above!)
    if "pseudomonas" in v or "belag, mäßiger exsudation" in v:
        return "Enthaltung / keine Angabe"
    if "unbekannt" in v or "nicht erkennbar" in v or "nicht ableitbar" in v or "nicht beurteilbar" in v or "unklar" in v or "nicht sicher beurteilbar" in v:
        return "Enthaltung / keine Angabe"

    return "Freitext belassen (Kein Matching)"
