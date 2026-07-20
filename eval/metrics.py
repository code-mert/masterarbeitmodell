from typing import Set, Tuple

def precision_recall(pred_set: Set[str], gt_set: Set[str]) -> Tuple[float, float]:
    """
    Calculates precision and recall between a predicted set and a ground truth set.
    Empty-set rules:
      - Both sets empty -> precision = 1.0, recall = 1.0
      - Exactly one set empty -> precision = 0.0, recall = 0.0
    """
    if not pred_set and not gt_set:
        return 1.0, 1.0
    if not pred_set or not gt_set:
        return 0.0, 0.0
        
    intersection = pred_set.intersection(gt_set)
    precision = len(intersection) / len(pred_set)
    recall = len(intersection) / len(gt_set)
    return precision, recall

def set_f1(pred_set: Set[str], gt_set: Set[str]) -> float:
    """
    Calculates the F1 score between a predicted set and a ground truth set.
    Empty-set rules:
      - Both sets empty -> F1 = 1.0
      - Exactly one set empty -> F1 = 0.0
    """
    if not pred_set and not gt_set:
        return 1.0
    if not pred_set or not gt_set:
        return 0.0
        
    precision, recall = precision_recall(pred_set, gt_set)
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def exact_match(pred_set: Set[str], gt_set: Set[str]) -> bool:
    """
    Checks if predicted set and ground truth set are identical (exact match).
    Empty-set rules:
      - Both sets empty -> True
      - Exactly one set empty -> False
    """
    if not pred_set and not gt_set:
        return True
    if not pred_set or not gt_set:
        return False
    return pred_set == gt_set

def best_path_f1(
    llm_praef: Set[str], llm_alt: Set[str], gt_praef: Set[str], gt_alt: Set[str]
) -> Tuple[float, bool, float, float]:
    """
    Calculates True Max-Path F1, Exact Match, Precision, and Recall across relevant path combinations.

    Returns:
        A tuple of (f1, exact_match_bool, precision, recall) for the best matching path.
    """
    paths = [(llm_praef, gt_praef)]
    if gt_alt:
        paths.append((llm_praef, gt_alt))
    if llm_alt:
        paths.append((llm_alt, gt_praef))
    if llm_alt or gt_alt:
        paths.append((llm_alt, gt_alt))

    best_f1 = -1.0
    best_exact = False
    best_prec = 0.0
    best_rec = 0.0

    for p_set, g_set in paths:
        prec, rec = precision_recall(p_set, g_set)
        f1_val = set_f1(p_set, g_set)
        exact_val = exact_match(p_set, g_set)

        if f1_val > best_f1:
            best_f1 = f1_val
            best_exact = exact_val
            best_prec = prec
            best_rec = rec

    return max(0.0, best_f1), best_exact, best_prec, best_rec
