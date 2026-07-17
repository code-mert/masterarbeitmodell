import json

# =====================================================================
# ORDINAL SCALES DEFINITIONS
# =====================================================================
ORDINAL_SCALES = {
    "exsudat": {
        "keine": 0,
        "keine, leicht": 0.5,
        "keine,leicht": 0.5,
        "leicht": 1,
        "leicht, mäßig": 1.5,
        "leicht, maessig": 1.5,
        "leicht,mäßig": 1.5,
        "leicht,maessig": 1.5,
        "mäßig": 2,
        "maessig": 2,
        "mäßig, stark": 2.5,
        "maessig, stark": 2.5,
        "mäßig,stark": 2.5,
        "maessig,stark": 2.5,
        "stark": 3,
        "stark, sehr stark": 3.5,
        "stark,sehr stark": 3.5,
        "sehr stark": 4
    },
    "infektion": {
        "keine infektionszeichen": 0, "keine": 0, "nein": 0,
        "verdacht auf infektion / kritische kolonisation": 1, "verdacht": 1,
        "deutliche infektionszeichen": 2, "deutliche": 2, "ja": 2
    }
}

# =====================================================================
# PURE SCORING & PARSING FUNCTIONS
# =====================================================================
def split_by_delimiters_outside_parentheses(text, delimiters=[','], strip=True):
    """
    Splits a string by given delimiters, but only if they are not inside parentheses
    or part of protected phrases.
    """
    if not isinstance(text, str):
        return [text]
    
    text_stripped = text.strip()
    
    # If the text is wrapped in brackets or quotes, it represents a quoted list of items
    starts_ends_quotes = (text_stripped.startswith('"') and text_stripped.endswith('"')) or \
                         (text_stripped.startswith("'") and text_stripped.endswith("'"))
    starts_ends_brackets = (text_stripped.startswith('[') and text_stripped.endswith(']'))
    
    if starts_ends_quotes or starts_ends_brackets:
        double_quotes_count = text_stripped.count('"')
        single_quotes_count = text_stripped.count("'")
        
        # If it uses double quotes, extract all double-quoted substrings
        if double_quotes_count >= 2:
            import re
            items = re.findall(r'"([^"]*)"', text_stripped)
            if items:
                return [p.strip() if strip else p for p in items if p.strip()]
                
        # If it uses single quotes, extract all single-quoted substrings
        if single_quotes_count >= 2:
            import re
            items = re.findall(r"'([^']*)'", text_stripped)
            if items:
                return [p.strip() if strip else p for p in items if p.strip()]
    
    # Define protected phrases (case-insensitive)
    protected_phrases = [
        "cvi-typische hautveränderungen (hyperpigmentierung, atrophie blanche, lipodermatosklerose)",
        "cvi-typische hautveränderungen (hyperppigmentierung, atropie blanche, lipodermatosklerose)",
        "cvi-typische hautveränderungen (hyperpigmentierung, atrophie blanche, lipdermatosklerose)",
        "autolytisch (hydrogele, hydrokolloide, folienverbände)",
        "mechanisch (monofilament-pad, feuchte kompressen, wundspülung)",
        "chirurgisch/scharf (skalpell, kürette)",
        "neutrale spüllösung (nacl, ringer)",
        "antimikrobielle spüllösung (phmb, octenisept)"
    ]
    
    temp_text = text
    replacements = {}
    for i, phrase in enumerate(protected_phrases):
        start = 0
        while True:
            idx = temp_text.lower().find(phrase, start)
            if idx == -1:
                break
            matched_text = temp_text[idx:idx+len(phrase)]
            placeholder = f"__PROTECTED_PHRASE_{i}__"
            replacements[placeholder] = matched_text
            temp_text = temp_text[:idx] + placeholder + temp_text[idx+len(phrase):]
            start = idx + len(placeholder)

    parts = []
    current = []
    depth = 0
    for char in temp_text:
        if char == '(':
            depth += 1
        elif char == ')':
            depth = max(0, depth - 1)
        
        if char in delimiters and depth == 0:
            part = "".join(current)
            if strip:
                part = part.strip()
            parts.append(part)
            current = []
        else:
            current.append(char)
    if current:
        part = "".join(current)
        if strip:
            part = part.strip()
        parts.append(part)
    
    # Restore replacements in split parts
    restored_parts = []
    for part in parts:
        for placeholder, original in replacements.items():
            part = part.replace(placeholder, original)
        restored_parts.append(part)
        
    return [p for p in restored_parts if p]

def to_clean_set(val):
    """
    Hilfsfunktion, um beliebige Zellwerte (JSON-Strings, kommagetrennte Strings, Listen)
    in ein Python-Set von bereinigten Lowercase-Strings zu konvertieren.
    Führt KEIN Spelling-Mapping oder typografische Ersetzungen durch.
    """
    if isinstance(val, (list, set, tuple)):
        items = [str(x) for x in val if x]
    elif isinstance(val, str):
        val_s = val.strip()
        if val_s.startswith('[') and val_s.endswith(']'):
            try:
                items = json.loads(val_s)
            except:
                items = split_by_delimiters_outside_parentheses(val_s)
        else:
            items = split_by_delimiters_outside_parentheses(val_s)
    else:
        items = [str(val)] if val is not None else []
        
    cleaned = set()
    for item in items:
        item_c = str(item).strip().lower()
        if item_c and item_c not in ["nan", "—", ""]:
            cleaned.add(item_c)
    return cleaned

def calculate_f1(set_a, set_b):
    """
    Berechnet den F1-Score zwischen zwei Sets.
    """
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    
    intersection = set_a.intersection(set_b)
    precision = len(intersection) / len(set_b)
    recall = len(intersection) / len(set_a)
    
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def best_path_f1(llm_p, llm_a, gt_p, gt_a):
    """
    Berechnet den F1-Score und Exact-Match für das vereinigte Produkt-Set
    (llm_p ∪ llm_a) vs (gt_p ∪ gt_a).
    """
    pred_set = llm_p | llm_a
    gt_set = gt_p | gt_a
    
    f1 = calculate_f1(pred_set, gt_set)
    exact = 1.0 if pred_set == gt_set else 0.0
    return f1, exact

def score_exact(gt_val, llm_val):
    """
    Berechnet ein einfaches Exact Match (1.0 oder 0.0).
    """
    gt_str = str(gt_val).strip().lower() if gt_val is not None else ""
    llm_str = str(llm_val).strip().lower() if llm_val is not None else ""
    if not gt_str and not llm_str:
        return 1.0
    return 1.0 if gt_str == llm_str else 0.0

def score_ordinal(category, gt_val, llm_val):
    """
    Berechnet den ordinalen Abstandsscore und das exakte Match für abgestufte Kategorien.
    """
    # 1. Konvertiere Werte zu bereinigten Strings
    gt_str = str(gt_val).strip().lower() if gt_val is not None else ""
    llm_str = str(llm_val).strip().lower() if llm_val is not None else ""
    
    # 2. Behandle leere / nicht angegebene Werte
    empty_values = ["", "nan", "—", "keine angabe", "keine angabe möglich", "keine einschätzung möglich", "nicht beurteilbar"]
    is_gt_empty = gt_str in empty_values
    is_llm_empty = llm_str in empty_values
    
    if is_gt_empty and is_llm_empty:
        return 1.0, 1.0
    if is_gt_empty or is_llm_empty:
        return 0.0, 0.0
        
    # 3. Hole die numerischen Werte aus der Skala
    scale = ORDINAL_SCALES[category]
    if gt_str not in scale or llm_str not in scale:
        return 0.0, 0.0
        
    gt_num = scale[gt_str]
    llm_num = scale[llm_str]
    
    max_val = max(scale.values())
    abs_diff = abs(gt_num - llm_num)
    
    score = 1.0 - (abs_diff / max_val)
    exact = 1.0 if abs_diff == 0 else 0.0
    return score, exact

def evaluate_checklist(gt_val, llm_val):
    """
    Berechnet F1 und Exact Match für Listen- bzw. Checklist-Werte.
    """
    gt_set = to_clean_set(gt_val)
    llm_set = to_clean_set(llm_val)
    
    f1 = calculate_f1(gt_set, llm_set)
    exact = 1.0 if gt_set == llm_set else 0.0
    return f1, exact
