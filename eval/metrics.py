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
    Calculates F1, Exact Match, Precision, and Recall for the combined union sets
    S_LLM = (llm_praef ∪ llm_alt) vs S_GT = (gt_praef ∪ gt_alt).
    This avoids empty-set matching artifacts on separate preference/alternative paths.

    Returns:
        A tuple of (f1, exact_match_bool, precision, recall) for the union sets.
    """
    pred_set = llm_praef | llm_alt
    gt_set = gt_praef | gt_alt

    precision, recall = precision_recall(pred_set, gt_set)
    f1 = set_f1(pred_set, gt_set)
    exact = exact_match(pred_set, gt_set)

    return f1, exact, precision, recall
