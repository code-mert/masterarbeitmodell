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
    Calculates the F1, Exact Match, Precision, and Recall for the best path out of the 
    4 cross-combinations (LLM path x GT path) based on maximizing the F1 score.
    Ties in F1 are broken by preferring exact matches.
    
    Returns:
        A tuple of (f1, exact_match_bool, precision, recall) for the best path.
    """
    combinations = [
        ("praef_praef", llm_praef, gt_praef),
        ("praef_alt", llm_praef, gt_alt),
        ("alt_praef", llm_alt, gt_praef),
        ("alt_alt", llm_alt, gt_alt),
    ]
    
    best_f1 = -1.0
    best_metrics = (0.0, False, 0.0, 0.0)
    
    for name, pred, gt in combinations:
        precision, recall = precision_recall(pred, gt)
        f1 = set_f1(pred, gt)
        exact = exact_match(pred, gt)
        
        if f1 > best_f1:
            best_f1 = f1
            best_metrics = (f1, exact, precision, recall)
        elif f1 == best_f1:
            # Tie breaker: if F1 is equal, choose the one with Exact Match
            if exact and not best_metrics[1]:
                best_metrics = (f1, exact, precision, recall)
                
    return best_metrics
