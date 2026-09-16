from collections import defaultdict

# ------------------------------------------------------------
# CS 4346 - Project #1 Part #1
# Binary PSR Rule Learning
#
# PSR(P) = n_plus(P) / n(P)
#
# n(P):
#     Number of rows where parameter P = 1
#
# n_plus(P):
#     Number of rows where parameter P = 1 AND Y = 1
# ------------------------------------------------------------

PARAMETERS = ["APP", "RAT", "INC", "BAL"]


DATA = [
    {"Label": 1,  "APP": 1, "RAT": 0, "INC": 0, "BAL": 1, "Y": 1},
    {"Label": 2,  "APP": 0, "RAT": 0, "INC": 1, "BAL": 0, "Y": 0},
    {"Label": 3,  "APP": 1, "RAT": 1, "INC": 0, "BAL": 1, "Y": 1},
    {"Label": 4,  "APP": 0, "RAT": 1, "INC": 1, "BAL": 1, "Y": 1},
    {"Label": 5,  "APP": 0, "RAT": 1, "INC": 1, "BAL": 0, "Y": 0},
    {"Label": 6,  "APP": 1, "RAT": 1, "INC": 1, "BAL": 0, "Y": 1},
    {"Label": 7,  "APP": 1, "RAT": 1, "INC": 1, "BAL": 1, "Y": 1},
    {"Label": 8,  "APP": 1, "RAT": 0, "INC": 1, "BAL": 0, "Y": 0},
    {"Label": 9,  "APP": 1, "RAT": 1, "INC": 0, "BAL": 0, "Y": 0},
    {"Label": 10, "APP": 0, "RAT": 0, "INC": 0, "BAL": 1, "Y": 0},
    {"Label": 11, "APP": 0, "RAT": 1, "INC": 0, "BAL": 1, "Y": 1},
    {"Label": 12, "APP": 1, "RAT": 0, "INC": 0, "BAL": 1, "Y": 1},
    {"Label": 13, "APP": 0, "RAT": 1, "INC": 1, "BAL": 1, "Y": 0},
    {"Label": 14, "APP": 1, "RAT": 0, "INC": 1, "BAL": 1, "Y": 1},
    {"Label": 15, "APP": 0, "RAT": 0, "INC": 1, "BAL": 1, "Y": 0},
]


def calculate_psr(rows, parameter):
    """
    Calculate numerator, denominator, and PSR for one parameter.
    """

    denominator = sum(
        1
        for row in rows
        if row[parameter] == 1
    )

    numerator = sum(
        1
        for row in rows
        if row[parameter] == 1 and row["Y"] == 1
    )

    if denominator == 0:
        psr = 0.0
    else:
        psr = numerator / denominator

    return numerator, denominator, psr


def print_psr_table(rows, parameters):
    """
    Display the PSR calculation for all available parameters.
    """

    print("\nPSR VALUES")
    print("-" * 50)
    print(
        f"{'Parameter':<12}"
        f"{'Numerator':>12}"
        f"{'Denominator':>14}"
        f"{'PSR':>10}"
    )
    print("-" * 50)

    for parameter in parameters:
        numerator, denominator, psr = calculate_psr(
            rows,
            parameter
        )

        print(
            f"{parameter:<12}"
            f"{numerator:>12}"
            f"{denominator:>14}"
            f"{psr:>10.3f}"
        )


def find_conflicts(rows):
    """
    Find rows having identical input parameters but different Y values.
    """

    groups = defaultdict(list)

    for row in rows:
        input_pattern = tuple(
            row[p]
            for p in PARAMETERS
        )

        groups[input_pattern].append(
            (row["Label"], row["Y"])
        )

    conflicts = []

    for input_pattern, values in groups.items():

        y_values = {
            y
            for label, y in values
        }

        if len(y_values) > 1:
            conflicts.append(
                (input_pattern, values)
            )

    return conflicts


def choose_best_parameter(rows, available_parameters):
    """
    Select the parameter having the highest PSR.

    Tie breaker:
    1. Higher PSR
    2. Larger denominator/support
    3. Original parameter order
    """

    candidates = []

    for parameter in available_parameters:

        numerator, denominator, psr = calculate_psr(
            rows,
            parameter
        )

        if denominator > 0 and numerator > 0:

            original_order = PARAMETERS.index(parameter)

            candidates.append(
                (
                    psr,
                    denominator,
                    -original_order,
                    parameter
                )
            )

    if not candidates:
        return None

    return max(candidates)[3]


def build_one_rule(rows):
    """
    Construct one rule using the greedy PSR method.
    """

    current_rows = list(rows)

    available_parameters = list(PARAMETERS)

    antecedent = []

    while any(
        row["Y"] == 0
        for row in current_rows
    ):

        print("\nCurrent rule:")

        if antecedent:
            print(
                " AND ".join(
                    f"{p}=1"
                    for p in antecedent
                )
            )
        else:
            print("<empty antecedent>")

        print(
            "Current labels:",
            [row["Label"] for row in current_rows]
        )

        print_psr_table(
            current_rows,
            available_parameters
        )

        best_parameter = choose_best_parameter(
            current_rows,
            available_parameters
        )

        if best_parameter is None:

            return (
                antecedent,
                current_rows,
                "No remaining parameter can "
                "specialize the rule further."
            )

        print(
            "\nSelected parameter:",
            best_parameter
        )

        antecedent.append(
            best_parameter
        )

        available_parameters.remove(
            best_parameter
        )

        current_rows = [
            row
            for row in current_rows
            if row[best_parameter] == 1
        ]

        if not current_rows:

            return (
                antecedent,
                current_rows,
                "Rule covers no rows."
            )

    return (
        antecedent,
        current_rows,
        None
    )


def rule_covers(row, antecedent):
    """
    A row is covered when every parameter
    in the rule antecedent equals 1.
    """

    return all(
        row[p] == 1
        for p in antecedent
    )


def generate_rules(rows):
    """
    Repeatedly create PSR rules.

    Positive examples covered by completed rules
    are removed.

    Negative examples remain in the working table.
    """

    positive_rows = [
        row
        for row in rows
        if row["Y"] == 1
    ]

    negative_rows = [
        row
        for row in rows
        if row["Y"] == 0
    ]

    rules = []

    rule_number = 1

    while positive_rows:

        print("\n")
        print("=" * 60)
        print(f"GENERATING RULE R{rule_number}")
        print("=" * 60)

        working_table = (
            positive_rows
            + negative_rows
        )

        antecedent, covered_rows, error = build_one_rule(
            working_table
        )

        if error:

            print("\nRULE GENERATION STOPPED")
            print(error)

            print(
                "Unresolved positive labels:",
                [
                    row["Label"]
                    for row in positive_rows
                ]
            )

            break

        covered_positive_labels = [
            row["Label"]
            for row in positive_rows
            if rule_covers(
                row,
                antecedent
            )
        ]

        rules.append(
            (
                antecedent,
                covered_positive_labels
            )
        )

        print("\nCompleted rule:")

        print(
            f"R{rule_number}: IF "
            + " AND ".join(
                f"{p}=1"
                for p in antecedent
            )
            + ", THEN Y=1"
        )

        print(
            "Positive labels covered:",
            covered_positive_labels
        )

        positive_rows = [
            row
            for row in positive_rows
            if row["Label"]
            not in covered_positive_labels
        ]

        rule_number += 1

    return rules


def main():

    print("=" * 60)
    print("CS 4346 - PROJECT #1 PART #1")
    print("BINARY PSR RULE LEARNING")
    print("=" * 60)

    print("\nInitial PSR computation:")

    print_psr_table(
        DATA,
        PARAMETERS
    )

    # Check for contradictory input patterns.
    conflicts = find_conflicts(DATA)

    if conflicts:

        print("\n")
        print("=" * 60)
        print("DATA CONFLICT DETECTED")
        print("=" * 60)

        for input_pattern, values in conflicts:

            pattern = ", ".join(
                f"{parameter}={value}"
                for parameter, value
                in zip(
                    PARAMETERS,
                    input_pattern
                )
            )

            print(
                "\nInput pattern:",
                pattern
            )

            for label, y in values:
                print(
                    f"Label {label}: Y={y}"
                )

        print(
            "\nIdentical input values have different "
            "target Y values."
        )

        print(
            "Therefore a deterministic rule set using "
            "only APP, RAT, INC, and BAL cannot perfectly "
            "classify every row."
        )

    # Generate PSR rules.
    rules = generate_rules(DATA)

    print("\n")
    print("=" * 60)
    print("FINAL GENERATED RULES")
    print("=" * 60)

    if not rules:

        print("No complete pure rules generated.")

    else:

        for number, (
            antecedent,
            labels
        ) in enumerate(
            rules,
            start=1
        ):

            rule_text = " AND ".join(
                f"{p}=1"
                for p in antecedent
            )

            print(
                f"R{number}: "
                f"IF {rule_text}, "
                f"THEN Y=1"
            )

            print(
                "    Covers positive labels:",
                labels
            )


if __name__ == "__main__":
    main()