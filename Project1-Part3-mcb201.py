from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# TABLE #3
# ============================================================

DATA = [
    {
        "Row": 1,
        "Rainfall": 625,
        "Avg_temp": 21.2,
        "Soil_pH": 6.5,
        "Nitrogen": 122,
        "Phosphorus": 49,
        "Field_size": 8.4,
        "Seeds": 22,
        "Irrigation": 36,
        "Crop_type": "Wheat",
        "Soil_type": "Loam",
        "Yield": 6.9,
    },
    {
        "Row": 2,
        "Rainfall": 485,
        "Avg_temp": 23.9,
        "Soil_pH": 5.9,
        "Nitrogen": 87,
        "Phosphorus": 33,
        "Field_size": 5.8,
        "Seeds": 20,
        "Irrigation": 23,
        "Crop_type": "Wheat",
        "Soil_type": "Sandy",
        "Yield": 4.8,
    },
    {
        "Row": 3,
        "Rainfall": 705,
        "Avg_temp": 20.4,
        "Soil_pH": 6.8,
        "Nitrogen": 133,
        "Phosphorus": 54,
        "Field_size": 12.1,
        "Seeds": 24,
        "Irrigation": 41,
        "Crop_type": "Corn",
        "Soil_type": "Loam",
        "Yield": 8.0,
    },
    {
        "Row": 4,
        "Rainfall": 400,
        "Avg_temp": 26.0,
        "Soil_pH": 5.7,
        "Nitrogen": 72,
        "Phosphorus": 29,
        "Field_size": 6.3,
        "Seeds": 18,
        "Irrigation": 19,
        "Crop_type": "Corn",
        "Soil_type": "Clay",
        "Yield": 4.1,
    },
    {
        "Row": 5,
        "Rainfall": 555,
        "Avg_temp": 23.0,
        "Soil_pH": 6.3,
        "Nitrogen": 112,
        "Phosphorus": 45,
        "Field_size": 9.5,
        "Seeds": 21,
        "Irrigation": 31,
        "Crop_type": "Wheat",
        "Soil_type": "Loam",
        "Yield": 6.2,
    },
    {
        "Row": 6,
        "Rainfall": 745,
        "Avg_temp": 19.8,
        "Soil_pH": 6.9,
        "Nitrogen": 143,
        "Phosphorus": 59,
        "Field_size": 13.8,
        "Seeds": 25,
        "Irrigation": 47,
        "Crop_type": "Corn",
        "Soil_type": "Loam",
        "Yield": 8.6,
    },
    {
        "Row": 7,
        "Rainfall": 435,
        "Avg_temp": 24.8,
        "Soil_pH": 5.8,
        "Nitrogen": 80,
        "Phosphorus": 31,
        "Field_size": 7.5,
        "Seeds": 19,
        "Irrigation": 21,
        "Crop_type": "Wheat",
        "Soil_type": "Sandy",
        "Yield": 4.3,
    },
    {
        "Row": 8,
        "Rainfall": 645,
        "Avg_temp": 21.2,
        "Soil_pH": 6.6,
        "Nitrogen": 123,
        "Phosphorus": 51,
        "Field_size": 10.3,
        "Seeds": 23,
        "Irrigation": 37,
        "Crop_type": "Corn",
        "Soil_type": "Loam",
        "Yield": 7.5,
    },
    {
        "Row": 9,
        "Rainfall": 590,
        "Avg_temp": 22.1,
        "Soil_pH": 6.4,
        "Nitrogen": 115,
        "Phosphorus": 46,
        "Field_size": 9.1,
        "Seeds": 22,
        "Irrigation": 33,
        "Crop_type": "Wheat",
        "Soil_type": "Loam",
        "Yield": 6.5,
    },
    {
        "Row": 10,
        "Rainfall": 520,
        "Avg_temp": 23.4,
        "Soil_pH": 6.1,
        "Nitrogen": 98,
        "Phosphorus": 39,
        "Field_size": 8.0,
        "Seeds": 21,
        "Irrigation": 27,
        "Crop_type": "Corn",
        "Soil_type": "Clay",
        "Yield": 5.6,
    },
    {
        "Row": 11,
        "Rainfall": 680,
        "Avg_temp": 20.8,
        "Soil_pH": 6.7,
        "Nitrogen": 130,
        "Phosphorus": 53,
        "Field_size": 11.6,
        "Seeds": 24,
        "Irrigation": 40,
        "Crop_type": "Corn",
        "Soil_type": "Loam",
        "Yield": 7.9,
    },
    {
        "Row": 12,
        "Rainfall": 455,
        "Avg_temp": 25.3,
        "Soil_pH": 5.7,
        "Nitrogen": 82,
        "Phosphorus": 34,
        "Field_size": 6.9,
        "Seeds": 19,
        "Irrigation": 24,
        "Crop_type": "Wheat",
        "Soil_type": "Sandy",
        "Yield": 4.6,
    },
    {
        "Row": 13,
        "Rainfall": 770,
        "Avg_temp": 19.3,
        "Soil_pH": 7.0,
        "Nitrogen": 150,
        "Phosphorus": 62,
        "Field_size": 14.4,
        "Seeds": 25,
        "Irrigation": 50,
        "Crop_type": "Corn",
        "Soil_type": "Loam",
        "Yield": 8.9,
    },
    {
        "Row": 14,
        "Rainfall": 570,
        "Avg_temp": 22.5,
        "Soil_pH": 6.2,
        "Nitrogen": 108,
        "Phosphorus": 43,
        "Field_size": 9.3,
        "Seeds": 22,
        "Irrigation": 32,
        "Crop_type": "Wheat",
        "Soil_type": "Loam",
        "Yield": 6.0,
    },
    {
        "Row": 15,
        "Rainfall": 610,
        "Avg_temp": 21.7,
        "Soil_pH": 6.5,
        "Nitrogen": 118,
        "Phosphorus": 47,
        "Field_size": 10.0,
        "Seeds": 23,
        "Irrigation": 35,
        "Crop_type": "Corn",
        "Soil_type": "Loam",
        "Yield": 7.1,
    },
]


NUMERIC_FEATURES = [
    "Rainfall",
    "Avg_temp",
    "Soil_pH",
    "Nitrogen",
    "Phosphorus",
    "Field_size",
    "Seeds",
    "Irrigation",
]

CATEGORICAL_FEATURES = [
    "Crop_type",
    "Soil_type",
]

FEATURE_ORDER = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# Minimum observations allowed in each final rule/group
MIN_LEAF = 2

# Used for floating-point equality when identifying ties
EPS = 1e-12


# ============================================================
# BASIC REGRESSION CALCULATIONS
# ============================================================

def mean_y(rows):
    return sum(row["Yield"] for row in rows) / len(rows)


def sse(rows):
    if not rows:
        return 0.0

    mean = mean_y(rows)

    return sum(
        (row["Yield"] - mean) ** 2
        for row in rows
    )


# ============================================================
# TREE DATA STRUCTURES
# ============================================================

@dataclass
class Split:
    feature: str
    kind: str

    reduction: float
    after_sse: float

    left: List[Dict[str, Any]]
    right: List[Dict[str, Any]]

    threshold: Optional[float] = None
    category: Optional[str] = None


@dataclass
class Node:
    rows: List[Dict[str, Any]]

    split: Optional[Split] = None

    left: Optional["Node"] = None
    right: Optional["Node"] = None


# ============================================================
# GENERATE ALL POSSIBLE SPLITS
# ============================================================

def candidate_splits(rows):

    parent_sse = sse(rows)

    candidates = []

    # --------------------------------------------------------
    # Numeric input parameters
    # --------------------------------------------------------

    for feature in NUMERIC_FEATURES:

        values = sorted(
            set(float(row[feature]) for row in rows)
        )

        # Test midpoint between adjacent distinct values
        for first, second in zip(values[:-1], values[1:]):

            threshold = (first + second) / 2.0

            left = [
                row
                for row in rows
                if float(row[feature]) <= threshold
            ]

            right = [
                row
                for row in rows
                if float(row[feature]) > threshold
            ]

            # Every final group must contain at least MIN_LEAF
            if len(left) < MIN_LEAF or len(right) < MIN_LEAF:
                continue

            after_sse = sse(left) + sse(right)

            reduction = parent_sse - after_sse

            candidates.append(
                Split(
                    feature=feature,
                    kind="numeric",
                    threshold=threshold,
                    reduction=reduction,
                    after_sse=after_sse,
                    left=left,
                    right=right,
                )
            )

    # --------------------------------------------------------
    # Categorical input parameters
    # --------------------------------------------------------

    for feature in CATEGORICAL_FEATURES:

        categories = sorted(
            set(str(row[feature]) for row in rows)
        )

        # Test each category against all other categories
        for category in categories:

            left = [
                row
                for row in rows
                if str(row[feature]) == category
            ]

            right = [
                row
                for row in rows
                if str(row[feature]) != category
            ]

            if len(left) < MIN_LEAF or len(right) < MIN_LEAF:
                continue

            after_sse = sse(left) + sse(right)

            reduction = parent_sse - after_sse

            candidates.append(
                Split(
                    feature=feature,
                    kind="categorical",
                    category=category,
                    reduction=reduction,
                    after_sse=after_sse,
                    left=left,
                    right=right,
                )
            )

    return candidates


# ============================================================
# SELECT BEST SPLIT
# ============================================================

def choose_best_split(rows):

    candidates = candidate_splits(rows)

    if not candidates:
        return None, []

    best_reduction = max(
        candidate.reduction
        for candidate in candidates
    )

    tied = [
        candidate
        for candidate in candidates
        if abs(candidate.reduction - best_reduction) <= EPS
    ]

    # --------------------------------------------------------
    # REQUIRED TIE BREAK:
    # If Rainfall is tied for the best reduction,
    # select Rainfall.
    # --------------------------------------------------------

    rainfall_ties = [
        candidate
        for candidate in tied
        if candidate.feature == "Rainfall"
    ]

    if rainfall_ties:

        rainfall_ties.sort(
            key=lambda candidate:
            candidate.threshold
            if candidate.threshold is not None
            else float("inf")
        )

        return rainfall_ties[0], tied

    # --------------------------------------------------------
    # If Rainfall is NOT part of the tie,
    # select according to the original input-column order.
    # --------------------------------------------------------

    def deterministic_key(candidate):

        feature_rank = FEATURE_ORDER.index(
            candidate.feature
        )

        if candidate.threshold is not None:
            value_rank = candidate.threshold
        else:
            value_rank = str(candidate.category)

        return feature_rank, str(value_rank)

    tied.sort(key=deterministic_key)

    return tied[0], tied


# ============================================================
# BUILD REGRESSION RULE TREE
# ============================================================

def build_tree(rows, depth=0):

    node = Node(rows=rows)

    best, tied = choose_best_split(rows)

    # Stop if no legal split exists
    # or the split does not reduce SSE.
    if best is None or best.reduction <= EPS:
        return node

    node.split = best

    indent = "  " * depth

    if best.kind == "numeric":

        split_text = (
            f"{best.feature} <= "
            f"{best.threshold:g}"
        )

    else:

        split_text = (
            f"{best.feature} == "
            f"{best.category}"
        )

    tied_features = sorted(
        set(candidate.feature for candidate in tied)
    )

    print(
        f"{indent}"
        f"Rows {[row['Row'] for row in rows]}: "
        f"SSE={sse(rows):.6f} -> "
        f"split on {split_text}; "
        f"after SSE={best.after_sse:.6f}; "
        f"reduction={best.reduction:.6f}"
    )

    if len(tied_features) > 1:

        print(
            f"{indent}  Equal-best features: "
            f"{', '.join(tied_features)}"
        )

        if "Rainfall" in tied_features:

            print(
                f"{indent}  Rainfall selected "
                f"by the required tie-break rule."
            )

    # Recursively create child nodes
    node.left = build_tree(
        best.left,
        depth + 1
    )

    node.right = build_tree(
        best.right,
        depth + 1
    )

    return node


# ============================================================
# COLLECT TERMINAL RULES
# ============================================================

def collect_leaves(node, path=None):

    if path is None:
        path = []

    if node.split is None:
        return [(path, node.rows)]

    split = node.split

    if split.kind == "numeric":

        left_condition = (
            split.feature,
            "<=",
            split.threshold
        )

        right_condition = (
            split.feature,
            ">",
            split.threshold
        )

    else:

        left_condition = (
            split.feature,
            "==",
            split.category
        )

        right_condition = (
            split.feature,
            "!=",
            split.category
        )

    return (
        collect_leaves(
            node.left,
            path + [left_condition]
        )
        +
        collect_leaves(
            node.right,
            path + [right_condition]
        )
    )


# ============================================================
# SIMPLIFY CONDITIONS
# ============================================================

def simplify_numeric_path(path):

    bounds = {}

    categorical_conditions = []

    for feature, operator, value in path:

        if feature in NUMERIC_FEATURES:

            if feature not in bounds:

                bounds[feature] = {
                    "lower": None,
                    "upper": None,
                }

            if operator == ">":

                current = bounds[feature]["lower"]

                if current is None:
                    bounds[feature]["lower"] = value
                else:
                    bounds[feature]["lower"] = max(
                        current,
                        value
                    )

            elif operator == "<=":

                current = bounds[feature]["upper"]

                if current is None:
                    bounds[feature]["upper"] = value
                else:
                    bounds[feature]["upper"] = min(
                        current,
                        value
                    )

        else:

            categorical_conditions.append(
                f"{feature} {operator} {value}"
            )

    conditions = []

    for feature in FEATURE_ORDER:

        if feature not in bounds:
            continue

        lower = bounds[feature]["lower"]
        upper = bounds[feature]["upper"]

        if lower is not None and upper is not None:

            conditions.append(
                f"{feature} > {lower:g} "
                f"AND {feature} <= {upper:g}"
            )

        elif lower is not None:

            conditions.append(
                f"{feature} > {lower:g}"
            )

        elif upper is not None:

            conditions.append(
                f"{feature} <= {upper:g}"
            )

    conditions.extend(
        categorical_conditions
    )

    return conditions


# ============================================================
# PRINT FINAL RULES
# ============================================================

def print_rules(tree):

    leaves = collect_leaves(tree)

    print()
    print("FINAL REGRESSION RULES")
    print("-" * 72)

    final_sse = 0.0

    for rule_number, (path, rows) in enumerate(
        leaves,
        start=1
    ):

        conditions = simplify_numeric_path(path)

        prediction = mean_y(rows)

        leaf_sse = sse(rows)

        final_sse += leaf_sse

        row_numbers = [
            row["Row"]
            for row in rows
        ]

        print(
            f"R{rule_number}: "
            f"IF {' AND '.join(conditions)}, "
            f"THEN Yield = "
            f"{prediction:.4f} t/ha"
        )

        print(
            f"    Rows: {row_numbers} "
            f"| Leaf SSE = "
            f"{leaf_sse:.6f}"
        )

    starting_sse = sse(DATA)

    print("-" * 72)

    print(
        f"Starting mean Yield = "
        f"{mean_y(DATA):.4f} t/ha"
    )

    print(
        f"Starting SSE        = "
        f"{starting_sse:.6f}"
    )

    print(
        f"Final SSE           = "
        f"{final_sse:.6f}"
    )

    print(
        f"Total SSE reduction = "
        f"{starting_sse - final_sse:.6f}"
    )

    print(
        f"Percent reduction   = "
        f"{((starting_sse - final_sse) / starting_sse) * 100:.4f}%"
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print(
        "REGRESSION-RULE LEARNING "
        "ON TABLE #3"
    )

    print(
        f"Minimum observations "
        f"per final group = {MIN_LEAF}"
    )

    print(
        "Tie-break rule: choose Rainfall "
        "whenever Rainfall is tied for "
        "best SSE reduction."
    )

    print()

    tree = build_tree(DATA)

    print_rules(tree)