from typing import List

from models.schemas import (
    FinalTestCase,
    ValidationIssue
)


VALID_PRIORITIES = {
    "Critical",
    "High",
    "Medium",
    "Low"
}


VALID_TYPES = {
    "Functional",
    "Negative",
    "Positive",
    "Edge",
    "Security",
    "SQL Injection",
    "Session",
    "Performance",
    "Accessibility",
    "Compatibility",
    "Cross-Browser",
    "Cross-Device",
    "Responsive",
    "Session Compatibility",
    "Mobile/Desktop"
}


def validate_test_cases(
    test_cases: List[FinalTestCase]
):

    issues = []

    test_ids = set()

    for test in test_cases:

        # ----------------------------------------------------
        # Duplicate Test ID
        # ----------------------------------------------------

        if test.test_id in test_ids:

            issues.append(
                ValidationIssue(
                    test_id=test.test_id,
                    issue_type="DUPLICATE_ID",
                    message=(
                        f"Duplicate test ID found: "
                        f"{test.test_id}"
                    ),
                    severity="High"
                )
            )

        test_ids.add(test.test_id)

        # ----------------------------------------------------
        # Test ID
        # ----------------------------------------------------

        if not test.test_id.strip():

            issues.append(
                ValidationIssue(
                    test_id=test.test_id,
                    issue_type="MISSING_ID",
                    message="Test ID is empty.",
                    severity="High"
                )
            )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        if not test.title.strip():

            issues.append(
                ValidationIssue(
                    test_id=test.test_id,
                    issue_type="MISSING_TITLE",
                    message="Test title is empty.",
                    severity="High"
                )
            )

        # ----------------------------------------------------
        # Priority
        # ----------------------------------------------------

        if test.priority not in VALID_PRIORITIES:

            issues.append(
                ValidationIssue(
                    test_id=test.test_id,
                    issue_type="INVALID_PRIORITY",
                    message=(
                        f"Invalid priority: "
                        f"{test.priority}"
                    ),
                    severity="Medium"
                )
            )

        # ----------------------------------------------------
        # Type
        # ----------------------------------------------------

        if test.type not in VALID_TYPES:

            issues.append(
                ValidationIssue(
                    test_id=test.test_id,
                    issue_type="INVALID_TYPE",
                    message=(
                        f"Unknown test type: "
                        f"{test.type}"
                    ),
                    severity="Low"
                )
            )

        # ----------------------------------------------------
        # Precondition
        # ----------------------------------------------------

        if not test.precondition.strip():

            issues.append(
                ValidationIssue(
                    test_id=test.test_id,
                    issue_type="MISSING_PRECONDITION",
                    message="Precondition is empty.",
                    severity="Medium"
                )
            )

        # ----------------------------------------------------
        # Steps
        # ----------------------------------------------------

        if not test.steps:

            issues.append(
                ValidationIssue(
                    test_id=test.test_id,
                    issue_type="MISSING_STEPS",
                    message="No test steps were provided.",
                    severity="High"
                )
            )

        else:

            for index, step in enumerate(
                test.steps,
                start=1
            ):

                if not step.strip():

                    issues.append(
                        ValidationIssue(
                            test_id=test.test_id,
                            issue_type="EMPTY_STEP",
                            message=(
                                f"Step {index} is empty."
                            ),
                            severity="High"
                        )
                    )

        # ----------------------------------------------------
        # Expected Result
        # ----------------------------------------------------

        if not test.expected_result.strip():

            issues.append(
                ValidationIssue(
                    test_id=test.test_id,
                    issue_type="MISSING_EXPECTED_RESULT",
                    message=(
                        "Expected result is empty."
                    ),
                    severity="High"
                )
            )

    return issues