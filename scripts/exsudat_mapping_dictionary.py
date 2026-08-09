import re
import pandas as pd

EXPLICIT_EXSUDAT_RULES = {
    # Keine (0)
    "keine": "Keine",
    "kein": "Keine",
    "trocken": "Keine",
    "vermutlich kaum": "Keine",
    "keine Angabe möglich, vermutlich trocken": "Keine",

    # Leicht (1)
    "leicht": "Leicht",
    "leicht ": "Leicht",
    "eher weniger": "Leicht",
    "eher wenig": "Leicht",
    "vermutlich wenig": "Leicht",
    "vermutlich gering": "Leicht",
    "keine Angabe möglich, vermutlich gering": "Leicht",
    "keine Angabe möglich / eher wenig": "Leicht",
    "keine Angabe möglich / vermutlich wenig": "Leicht",
    "schwach": "Leicht",
    "schwach ": "Leicht",
    "könnte eher schwach sein": "Leicht",
    "sehr gering": "Leicht",

    # Mäßig (2)
    "mäßig": "Mäßig",
    "mäfig": "Mäßig",
    " mäßig": "Mäßig",
    "Mässig": "Mäßig",
    "vermutlich mäßig": "Mäßig",
    "vermutlich mässig": "Mäßig",
    "vermutlich mittelmässig": "Mäßig",
    "vermutlich mittelmäßig": "Mäßig",
    "vermutlich mittel": "Mäßig",
    "mittel": "Mäßig",
    "mittelstark": "Mäßig",
    "keine Angabe möglich / vermutlich mässig": "Mäßig",
    "wahrscheinlich mittelmäßig vorhanden": "Mäßig",
    "blutig bis serös teilweise vorhanden dann eher mäßig": "Mäßig",
    "scheint mäßig zu sein": "Mäßig",
    "nicht genau definierbar, aus der Erfahrung heraus mäßige Exsudation": "Mäßig",
    "Nekrosen: kein Exsudat. Unterschenkel mäßig": "Mäßig",

    # Stark (3)
    "stark": "Stark",
    "Annahme stark": "Stark",
    "vermutlich hoch": "Stark",
    "vermutlich hohe Exsudation": "Stark",
    "vermutlich starke Exsudation": "Stark",
    "nicht beurteilbar, vermutlich stark": "Stark",
    "warsch hoch bis sehr hoch,  klare exsudation": "Stark",
    "Große Wunde: stark, da Mazerationen am Wundrand\nKleine Nekrose: trocken": "Stark",

    # Range: Keine, Leicht ({0, 1})
    "keine genaue Angabe möglich, sieht eher trocken bis leicht exsudierend aus": "Keine, Leicht",
    "schwach bis nicht vorhanden": "Keine, Leicht",
    "gering bis gar nicht": "Keine, Leicht",
    "offenen stelle mäßig, geschlossene stelle kein bis wenig exsudat": "Keine, Leicht",

    # Range: Leicht, Mäßig ({1, 2})
    "leicht bis mittel": "Leicht, Mäßig",
    "leicht bis mäßig": "Leicht, Mäßig",
    "schwach bis mäßig": "Leicht, Mäßig",
    "schwach bin mäßig": "Leicht, Mäßig",
    "eher schwach b is mäßig": "Leicht, Mäßig",
    "leichte bis mäßige exsudation": "Leicht, Mäßig",

    # Range: Mäßig, Stark ({2, 3})
    "mäßig bis stark": "Mäßig, Stark",
    "mittel bis stark": "Mäßig, Stark",
    "mäßig bis stark, sicher ist eine Geruchsbildung süßlich aromatisch teilweise beschrieben als traubenartig": "Mäßig, Stark",
}

def map_exsudat_explicit(val):
    if pd.isna(val) or val == "" or val is None or val == "?" or val == "???":
        return "Enthaltung / keine Angabe"

    val_str = str(val).strip()
    val_lower = val_str.lower()

    # Exact dictionary lookup first
    if val_str in EXPLICIT_EXSUDAT_RULES:
        return EXPLICIT_EXSUDAT_RULES[val_str]
    if val_lower in EXPLICIT_EXSUDAT_RULES:
        return EXPLICIT_EXSUDAT_RULES[val_lower]

    # Explicit refusal terms
    if any(term == val_lower or val_lower.startswith(term) for term in [
        "keine angabe möglich", "keine einschätzung möglich", "nicht zu beschreiben",
        "nicht beurteilbar", "vermutlich vorhanden, in welcher menge ist nicht zu beurteilen",
        "nicht klar, eher trübe wunde könnte geruch abgeben", "keine angabe", "n/a", "[]", "nan"
    ]):
        return "Enthaltung / keine Angabe"

    # Multi-range values
    if "keine, leicht" in val_lower or "leicht, keine" in val_lower:
        return "Keine, Leicht"
    if "leicht, mäßig" in val_lower or "mäßig, leicht" in val_lower:
        return "Leicht, Mäßig"
    if "mäßig, stark" in val_lower or "stark, mäßig" in val_lower:
        return "Mäßig, Stark"
    if "stark, sehr stark" in val_lower:
        return "Stark"

    # Pattern matching fallback
    if "stark" in val_lower or "hoch" in val_lower:
        return "Stark"
    if "mäßig" in val_lower or "mässig" in val_lower or "mittel" in val_lower:
        return "Mäßig"
    if "leicht" in val_lower or "gering" in val_lower or "schwach" in val_lower or "wenig" in val_lower:
        return "Leicht"
    if "kein" in val_lower or "trocken" in val_lower or "kaum" in val_lower:
        return "Keine"

    return "Enthaltung / keine Angabe"

def get_exsudat_ranks(mapped_val):
    """
    Returns a set of numerical rank integers for ordinal evaluation:
    Keine = 0, Leicht = 1, Mäßig = 2, Stark = 3.
    """
    if mapped_val == "Keine":
        return {0}
    if mapped_val == "Leicht":
        return {1}
    if mapped_val == "Mäßig":
        return {2}
    if mapped_val == "Stark":
        return {3}
    if mapped_val == "Keine, Leicht":
        return {0, 1}
    if mapped_val == "Leicht, Mäßig":
        return {1, 2}
    if mapped_val == "Mäßig, Stark":
        return {2, 3}
    return set()

def calculate_ordinal_score(ki_mapped, exp_mapped):
    """
    Calculates ordinal similarity score between 0.0 and 1.0 (0% to 100%).
    Score(d) = 1.0 - (d / 3.0)
    d = min absolute distance between rank sets.
    """
    ki_ranks = get_exsudat_ranks(ki_mapped)
    exp_ranks = get_exsudat_ranks(exp_mapped)

    if not ki_ranks or not exp_ranks:
        return None  # Enthaltung / N/A

    min_dist = min(abs(r_ki - r_exp) for r_ki in ki_ranks for r_exp in exp_ranks)
    score = 1.0 - (min_dist / 3.0)
    return score
