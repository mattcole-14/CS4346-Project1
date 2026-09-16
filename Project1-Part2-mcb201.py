# CS 4346 Project #1 - Part #2
# PSR rule learning after converting non-binary inputs
# into binary conditions.

COLUMNS = [
    "row", "age", "income", "credit", "loan", "dti",
    "job", "interest", "term", "housing", "purpose", "Y"
]

RAW_ROWS = [
    (1, 25, 40, 615, 19, 41, 1, 18.1, 60, "Rent", "Auto", 1),
    (2, 44, 90, 755, 21, 20, 10, 7.5, 36, "Own", "Home improvement", 0),
    (3, 32, 57, 670, 16, 34, 4, 13.4, 48, "Rent", "Education", 1),
    (4, 51, 115, 800, 24, 15, 17, 6.2, 36, "Own", "Auto", 0),
    (5, 29, 49, 635, 13, 38, 2, 15.8, 60, "Rent", "Medical", 1),
    (6, 40, 78, 715, 11, 23, 8, 9.1, 36, "Mortgage", "Home improvement", 0),
    (7, 35, 65, 685, 21, 30, 6, 11.4, 48, "Rent", "Business", 0),
    (8, 27, 44, 612, 17, 45, 1, 18.8, 60, "Rent", "Education", 1),
    (9, 47, 96, 770, 18, 18, 12, 6.9, 36, "Own", "Auto", 0),
    (10, 30, 53, 650, 14, 36, 3, 14.6, 48, "Rent", "Medical", 1),
    (11, 54, 122, 815, 27, 13, 20, 5.5, 36, "Own", "Home improvement", 0),
    (12, 38, 72, 705, 12, 26, 7, 9.8, 48, "Mortgage", "Business", 0),
    (13, 23, 36, 600, 20, 47, 0, 19.5, 60, "Rent", "Education", 1),
    (14, 42, 84, 735, 16, 22, 9, 8.3, 36, "Own", "Auto", 0),
    (15, 33, 60, 675, 23, 33, 5, 12.5, 48, "Rent", "Business", 1),
]

DATA = [dict(zip(COLUMNS, row)) for row in RAW_ROWS]

# Feature order is also used as the final tie-break order.
FEATURES = [
    "AGE",
    "INCOME",
    "CREDIT",
    "LOAN",
    "DTI",
    "JOB",
    "INTEREST",
    "TERM",
    "HOUSING",
    "PURPOSE",
]

CONDITION_TEXT = {
    "AGE": "Age <= 30",
    "INCOME": "Annual income <= 55 ($k)",
    "CREDIT": "Credit score <= 665",
    "LOAN": "Loan >= 12 ($k)",
    "DTI": "Debt/income >= 35%",
    "JOB": "Job years <= 4",
    "INTEREST": "Interest >= 13.8%",
    "TERM": "Loan term = 60 months",
    "HOUSING": "Housing = Rent",
    "PURPOSE": "Loan purpose = Education",
}


def convert_row(r):
    """Convert one original Table #2 row to binary values."""
    return {
        "row": r["row"],
        "AGE": int(r["age"] <= 30),
        "INCOME": int(r["income"] <= 55),
        "CREDIT": int(r["credit"] <= 665),
        "LOAN": int(r["loan"] >= 12),
        "DTI": int(r["dti"] >= 35),
        "JOB": int(r["job"] <= 4),
        "INTEREST": int(r["interest"] >= 13.8),
        "TERM": int(r["term"] == 60),
        "HOUSING": int(r["housing"] == "Rent"),
        "PURPOSE": int(r["purpose"] == "Education"),
        "Y": r["Y"],
    }


BINARY = [convert_row(row) for row in DATA]


def psr(rows, feature):
    """
    PSR(P) = nP+ / nP

    nP  = number of rows where P = 1
    nP+ = number of those rows where Y = 1
    """
    denominator = sum(row[feature] == 1 for row in rows)

    numerator = sum(
        row[feature] == 1 and row["Y"] == 1
        for row in rows
    )

    if denominator == 0:
        return numerator, denominator, 0.0

    return numerator, denominator, numerator / denominator


def choose_best(rows, available_features):
    """
    Choose the parameter with the highest PSR.

    Tie #1:
        Choose the parameter with larger support/denominator.

    Tie #2:
        Choose whichever occurs earlier in FEATURES.
    """
    best = None

    for order, feature in enumerate(FEATURES):

        if feature not in available_features:
            continue

        numerator, denominator, ratio = psr(rows, feature)

        # P=1 covers no rows, so the parameter cannot reduce the table.
        if denominator == 0:
            continue

        candidate = (
            ratio,
            denominator,
            -order,
            feature
        )

        if best is None or candidate > best:
            best = candidate

    if best is None:
        return None

    return best[3]


def print_binary_table():
    """Print the complete modified binary table."""
    headers = ["row"] + FEATURES + ["Y"]

    print("\nMODIFIED BINARY TABLE #2")
    print(" ".join(f"{header:>8}" for header in headers))
    print("-" * (9 * len(headers)))

    for row in BINARY:
        print(
            " ".join(
                f"{row[header]:>8}"
                for header in headers
            )
        )


def print_initial_psr():
    """Compute and print initial PSR values."""
    print("\nINITIAL PSR VALUES")

    print(
        f"{'Parameter':<12}"
        f"{'nP+':>6}"
        f"{'nP':>6}"
        f"{'PSR':>9}   Condition"
    )

    print("-" * 78)

    for feature in FEATURES:

        numerator, denominator, ratio = psr(
            BINARY,
            feature
        )

        print(
            f"{feature:<12}"
            f"{numerator:>6}"
            f"{denominator:>6}"
            f"{ratio:>9.3f}   "
            f"{CONDITION_TEXT[feature]}"
        )


def find_binary_conflicts(rows):
    """
    Find positive and negative rows that have exactly
    the same binary input vector.
    """
    conflicts = []

    for i, first in enumerate(rows):

        for second in rows[i + 1:]:

            same_inputs = all(
                first[feature] == second[feature]
                for feature in FEATURES
            )

            opposite_targets = (
                first["Y"] != second["Y"]
            )

            if same_inputs and opposite_targets:

                conflicts.append(
                    (first["row"], second["row"])
                )

    return conflicts


def generate_rules(rows):
    """
    Generate rules using the PSR algorithm from the course.

    After a complete rule is found:
    - Remove the positive rows it covers.
    - Keep all negative rows.
    - Begin learning the next rule.
    """
    rules = []

    uncovered_positives = {
        row["row"]
        for row in rows
        if row["Y"] == 1
    }

    rule_number = 1

    while uncovered_positives:

        # New table contains:
        # all negatives
        # +
        # positive rows not already covered
        current = [
            row
            for row in rows
            if (
                row["Y"] == 0
                or row["row"] in uncovered_positives
            )
        ]

        available = FEATURES.copy()
        antecedent = []

        # Continue specializing while negative rows remain.
        while any(row["Y"] == 0 for row in current):

            feature = choose_best(
                current,
                available
            )

            if feature is None:

                print(
                    f"\nR{rule_number} "
                    f"cannot be completed."
                )

                if antecedent:
                    print(
                        "Current antecedent: "
                        + " AND ".join(
                            f"{f}=1"
                            for f in antecedent
                        )
                    )

                print(
                    "Rows still covered:",
                    [row["row"] for row in current]
                )

                return (
                    rules,
                    sorted(uncovered_positives)
                )

            numerator, denominator, ratio = psr(
                current,
                feature
            )

            print(
                f"R{rule_number} select {feature}: "
                f"{numerator}/{denominator} "
                f"= {ratio:.3f}"
            )

            antecedent.append(feature)

            available.remove(feature)

            # Construct the next reduced table.
            current = [
                row
                for row in current
                if row[feature] == 1
            ]

            # A valid rule must still cover a positive row.
            if not any(
                row["Y"] == 1
                for row in current
            ):

                print(
                    f"\nR{rule_number} "
                    "lost all positive rows."
                )

                return (
                    rules,
                    sorted(uncovered_positives)
                )

        # No negative rows remain: completed rule.
        covered = [
            row["row"]
            for row in current
            if row["Y"] == 1
        ]

        rules.append(
            (
                rule_number,
                antecedent.copy(),
                covered
            )
        )

        uncovered_positives.difference_update(
            covered
        )

        print(
            f"\nR{rule_number}: IF "
            + " AND ".join(
                f"{feature}=1"
                for feature in antecedent
            )
            + ", THEN Y=1"
        )

        print(
            "Covered positive rows:",
            covered
        )

        rule_number += 1

    return rules, []


# ============================================================
# MAIN PROGRAM
# ============================================================

print("BINARY CONDITIONS")
print("-" * 70)

for feature in FEATURES:
    print(
        f"{feature:<10} -> "
        f"{CONDITION_TEXT[feature]}"
    )


print_binary_table()

print_initial_psr()


print("\nRULE GENERATION")
print("=" * 70)

rules, unresolved = generate_rules(
    BINARY
)


print("\nFINAL COMPLETED RULES")
print("=" * 70)

if rules:

    for number, antecedent, covered in rules:

        print(
            f"R{number}: IF "
            + " AND ".join(
                f"{feature}=1"
                for feature in antecedent
            )
            + f", THEN Y=1 "
              f"(covers rows {covered})"
        )

else:
    print("No completed rules were generated.")


if unresolved:

    print(
        "\nUnresolved positive rows:",
        unresolved
    )

    conflicts = find_binary_conflicts(
        BINARY
    )

    if conflicts:

        print(
            "\nBinary-input conflicts "
            "(same inputs but opposite Y):"
        )

        for first, second in conflicts:
            print(
                f"Rows {first} and {second}"
            )