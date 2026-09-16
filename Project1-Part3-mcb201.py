# CS 4346 Project #1 - Part #2
# Non-binary inputs converted to binary conditions
# PSR Rule Learning Method

COLUMNS = [
    "row",
    "age",
    "income",
    "credit",
    "loan",
    "dti",
    "job",
    "interest",
    "term",
    "housing",
    "purpose",
    "Y"
]

RAW_ROWS = [
    (1, 25, 40, 615, 19, 41, 1, 18.1, 60, "Rent", "Auto", 1),
    (2, 44, 90, 755, 21, 20, 10, 7.5, 36, "Own",
     "Home improvement", 0),
    (3, 32, 57, 670, 16, 34, 4, 13.4, 48, "Rent",
     "Education", 1),
    (4, 51, 115, 800, 24, 15, 17, 6.2, 36, "Own",
     "Auto", 0),
    (5, 29, 49, 635, 13, 38, 2, 15.8, 60, "Rent",
     "Medical", 1),
    (6, 40, 78, 715, 11, 23, 8, 9.1, 36, "Mortgage",
     "Home improvement", 0),
    (7, 35, 65, 685, 21, 30, 6, 11.4, 48, "Rent",
     "Business", 0),
    (8, 27, 44, 612, 17, 45, 1, 18.8, 60, "Rent",
     "Education", 1),
    (9, 47, 96, 770, 18, 18, 12, 6.9, 36, "Own",
     "Auto", 0),
    (10, 30, 53, 650, 14, 36, 3, 14.6, 48, "Rent",
     "Medical", 1),
    (11, 54, 122, 815, 27, 13, 20, 5.5, 36, "Own",
     "Home improvement", 0),
    (12, 38, 72, 705, 12, 26, 7, 9.8, 48, "Mortgage",
     "Business", 0),
    (13, 23, 36, 600, 20, 47, 0, 19.5, 60, "Rent",
     "Education", 1),
    (14, 42, 84, 735, 16, 22, 9, 8.3, 36, "Own",
     "Auto", 0),
    (15, 33, 60, 675, 23, 33, 5, 12.5, 48, "Rent",
     "Business", 1)
]

DATA = [
    dict(zip(COLUMNS, row))
    for row in RAW_ROWS
]


# ------------------------------------------------------------
# Binary parameters
# ------------------------------------------------------------

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
    "PURPOSE"
]


CONDITION_TEXT = {
    "AGE": "Age <= 33",
    "INCOME": "Annual income <= 60 ($k)",
    "CREDIT": "Credit score <= 675",
    "LOAN": "Loan <= 20 ($k)",
    "DTI": "Debt/income >= 33%",
    "JOB": "Job years <= 5",
    "INTEREST": "Interest >= 12.5%",
    "TERM": "Loan term = 60 months",
    "HOUSING": "Housing = Rent",
    "PURPOSE": "Loan purpose = Education"
}


def convert_row(row):
    """
    Convert one original non-binary row into a binary row.

    A value of 1 means the condition is satisfied.
    A value of 0 means the condition is not satisfied.
    """

    return {
        "row": row["row"],

        "AGE":
            int(row["age"] <= 33),

        "INCOME":
            int(row["income"] <= 60),

        "CREDIT":
            int(row["credit"] <= 675),

        "LOAN":
            int(row["loan"] <= 20),

        "DTI":
            int(row["dti"] >= 33),

        "JOB":
            int(row["job"] <= 5),

        "INTEREST":
            int(row["interest"] >= 12.5),

        "TERM":
            int(row["term"] == 60),

        "HOUSING":
            int(row["housing"] == "Rent"),

        "PURPOSE":
            int(row["purpose"] == "Education"),

        "Y":
            row["Y"]
    }


BINARY = [
    convert_row(row)
    for row in DATA
]


# ------------------------------------------------------------
# PSR calculation
# ------------------------------------------------------------

def psr(rows, feature):
    """
    Compute:

        PSR(P) = nP+ / nP

    nP:
        Number of instances where P = 1.

    nP+:
        Number of instances where P = 1
        and Y = 1.
    """

    denominator = sum(
        row[feature] == 1
        for row in rows
    )

    numerator = sum(
        row[feature] == 1
        and row["Y"] == 1
        for row in rows
    )

    if denominator == 0:
        return numerator, denominator, 0.0

    ratio = numerator / denominator

    return numerator, denominator, ratio


# ------------------------------------------------------------
# Parameter selection
# ------------------------------------------------------------

def choose_best(rows, available_features):
    """
    Select the feature with the highest PSR.

    Tie-breaking:

    1. Higher PSR wins.
    2. If PSRs tie, larger denominator/support wins.
    3. If both still tie, use original FEATURES order.

    The third tie-break simply makes execution deterministic.
    """

    best_feature = None
    best_ratio = -1.0
    best_support = -1

    for feature in FEATURES:

        if feature not in available_features:
            continue

        numerator, denominator, ratio = psr(
            rows,
            feature
        )

        # A feature covering no rows cannot be selected.
        if denominator == 0:
            continue

        better_psr = ratio > best_ratio

        same_psr_better_support = (
            ratio == best_ratio
            and denominator > best_support
        )

        if (
            better_psr
            or same_psr_better_support
        ):
            best_feature = feature
            best_ratio = ratio
            best_support = denominator

    return best_feature


# ------------------------------------------------------------
# Display functions
# ------------------------------------------------------------

def print_conditions():

    print("BINARY CONDITIONS")
    print("-" * 70)

    for feature in FEATURES:
        print(
            f"{feature:<10} -> "
            f"{CONDITION_TEXT[feature]}"
        )


def print_binary_table():

    headers = (
        ["row"]
        + FEATURES
        + ["Y"]
    )

    print("\nMODIFIED BINARY TABLE #2")

    print(
        " ".join(
            f"{header:>9}"
            for header in headers
        )
    )

    print(
        "-" * (10 * len(headers))
    )

    for row in BINARY:

        print(
            " ".join(
                f"{row[header]:>9}"
                for header in headers
            )
        )


def print_initial_psr():

    print("\nINITIAL PSR VALUES")

    print(
        f"{'Parameter':<12}"
        f"{'nP+':>6}"
        f"{'nP':>6}"
        f"{'PSR':>10}   "
        f"Condition"
    )

    print("-" * 82)

    for feature in FEATURES:

        numerator, denominator, ratio = psr(
            BINARY,
            feature
        )

        print(
            f"{feature:<12}"
            f"{numerator:>6}"
            f"{denominator:>6}"
            f"{ratio:>10.3f}   "
            f"{CONDITION_TEXT[feature]}"
        )


# ------------------------------------------------------------
# Conflict checking
# ------------------------------------------------------------

def find_binary_conflicts(rows):
    """
    Find rows having identical binary inputs
    but opposite Y values.
    """

    conflicts = []

    for i in range(len(rows)):

        first = rows[i]

        for j in range(i + 1, len(rows)):

            second = rows[j]

            same_inputs = all(
                first[feature]
                == second[feature]
                for feature in FEATURES
            )

            opposite_y = (
                first["Y"]
                != second["Y"]
            )

            if same_inputs and opposite_y:

                conflicts.append(
                    (
                        first["row"],
                        second["row"]
                    )
                )

    return conflicts


# ------------------------------------------------------------
# PSR rule generation
# ------------------------------------------------------------

def generate_rules(rows):
    """
    Generate rules using the PSR algorithm.

    Procedure:

    1. Start with all uncovered positive rows
       and all negative rows.

    2. Compute PSR for each available parameter.

    3. Choose the parameter with the highest PSR.

    4. Restrict the current table to rows where
       that parameter equals 1.

    5. Continue adding parameters while the
       provisional rule still covers negatives.

    6. Once no negatives remain, save the rule.

    7. Remove the positive rows covered by the
       completed rule, but retain all negatives.

    8. Repeat until every positive instance
       is covered.
    """

    rules = []

    uncovered_positives = {
        row["row"]
        for row in rows
        if row["Y"] == 1
    }

    rule_number = 1

    while uncovered_positives:

        # Keep:
        # all negative rows
        # plus positive rows not covered yet.
        current = [
            row
            for row in rows
            if (
                row["Y"] == 0
                or
                row["row"]
                in uncovered_positives
            )
        ]

        available_features = FEATURES.copy()

        antecedent = []

        print(
            f"\nStarting R{rule_number}"
        )

        # Continue specializing while negatives remain.
        while any(
            row["Y"] == 0
            for row in current
        ):

            feature = choose_best(
                current,
                available_features
            )

            if feature is None:

                print(
                    f"R{rule_number} "
                    "cannot be completed."
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
                f"R{rule_number} select "
                f"{feature}: "
                f"{numerator}/{denominator} "
                f"= {ratio:.3f}"
            )

            antecedent.append(feature)

            available_features.remove(
                feature
            )

            # Reduce table to rows satisfying
            # the selected parameter.
            current = [
                row
                for row in current
                if row[feature] == 1
            ]

            # Safety check:
            # the rule must still cover
            # at least one positive instance.
            if not any(
                row["Y"] == 1
                for row in current
            ):

                print(
                    f"R{rule_number} "
                    "lost all positive instances."
                )

                return (
                    rules,
                    sorted(uncovered_positives)
                )

        # At this point the provisional rule
        # covers no negative instances.
        covered_positive_rows = [
            row["row"]
            for row in current
            if row["Y"] == 1
        ]

        rules.append(
            (
                rule_number,
                antecedent.copy(),
                covered_positive_rows
            )
        )

        uncovered_positives.difference_update(
            covered_positive_rows
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
            covered_positive_rows
        )

        rule_number += 1

    return rules, []


# ------------------------------------------------------------
# Main program
# ------------------------------------------------------------

print_conditions()

print_binary_table()

print_initial_psr()


print("\nBINARY CONFLICT CHECK")
print("=" * 70)

conflicts = find_binary_conflicts(
    BINARY
)

if conflicts:

    print(
        "Conflicts found:"
    )

    for first, second in conflicts:

        print(
            f"Rows {first} and {second}"
        )

else:

    print(
        "No binary-input conflicts found."
    )


print("\nRULE GENERATION")
print("=" * 70)

rules, unresolved = generate_rules(
    BINARY
)


print("\nFINAL COMPLETED RULES")
print("=" * 70)

if rules:

    for (
        number,
        antecedent,
        covered
    ) in rules:

        print(
            f"R{number}: IF "
            + " AND ".join(
                f"{feature}=1"
                for feature in antecedent
            )
            + ", THEN Y=1 "
            + f"(covers rows {covered})"
        )

else:

    print(
        "No completed rules generated."
    )


if unresolved:

    print(
        "\nUnresolved positive rows:",
        unresolved
    )

else:

    print(
        "\nAll positive instances "
        "are covered."
    )