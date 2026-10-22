from models.schemas import (
    FinalTestSuite,
    ApprovedTestCase,
    ValidatedTestSuite
)

from validators.qa_validator import (
    validate_test_cases
)

from validators.duplicate_detector import (
    find_duplicate_tests
)

from validators.quality_scorer import (
    calculate_quality_score
)


QUALITY_APPROVAL_THRESHOLD = 70


def validate_test_suite(
    final_suite: FinalTestSuite
) -> ValidatedTestSuite:

    test_cases = final_suite.test_cases

    # ========================================================
    # STEP 1 — Deterministic Validation
    # ========================================================

    validation_issues = validate_test_cases(
        test_cases
    )

    # ========================================================
    # STEP 2 — Duplicate Detection
    # ========================================================

    unique_tests, duplicates = (
        find_duplicate_tests(
            test_cases
        )
    )

    # ========================================================
    # Add duplicate issues
    # ========================================================

    for duplicate in duplicates:

        duplicate_test_id = duplicate[0]

        duplicate_of = duplicate[1]

        reason = duplicate[2]

        from models.schemas import ValidationIssue

        validation_issues.append(
            ValidationIssue(
                test_id=duplicate_test_id,
                issue_type="DUPLICATE_TEST",
                message=(
                    f"Duplicate of {duplicate_of}: "
                    f"{reason}"
                ),
                severity="Medium"
            )
        )

    # ========================================================
    # STEP 3 — Quality Scoring
    # ========================================================

    approved_tests = []

    for test in unique_tests:

        quality = calculate_quality_score(
            test
        )

        # ----------------------------------------------------
        # Determine validation status
        # ----------------------------------------------------

        test_issues = [
            issue
            for issue in validation_issues
            if issue.test_id == test.test_id
        ]

        has_high_severity_issue = any(
            issue.severity == "High"
            for issue in test_issues
        )

        if (
            quality.score
            >= QUALITY_APPROVAL_THRESHOLD
            and not has_high_severity_issue
        ):

            validation_status = "Approved"

        else:

            validation_status = "Needs Review"

        # ----------------------------------------------------
        # Create approved test object
        # ----------------------------------------------------

        approved_tests.append(
            ApprovedTestCase(
                test_id=test.test_id,
                title=test.title,
                type=test.type,
                priority=test.priority,
                precondition=test.precondition,
                steps=test.steps,
                expected_result=test.expected_result,
                source_agent=test.source_agent,
                quality_score=quality.score,
                quality_status=quality.status,
                validation_status=validation_status
            )
        )

    # ========================================================
    # STEP 4 — Recalculate Coverage
    # ========================================================

    approved_only = [
        test
        for test in approved_tests
        if test.validation_status == "Approved"
    ]

    coverage = final_suite.coverage.model_copy(
        update={
            "total_tests": len(approved_only),

            "functional": sum(
                1
                for test in approved_only
                if test.type == "Functional"
            ),

            "security": sum(
                1
                for test in approved_only
                if (
                    test.type == "Security"
                    or test.type == "SQL Injection"
                )
            ),

            "session": sum(
                1
                for test in approved_only
                if "Session" in test.type
            ),

            "performance": sum(
                1
                for test in approved_only
                if test.type == "Performance"
            ),

            "accessibility": sum(
                1
                for test in approved_only
                if test.type == "Accessibility"
            ),

            "compatibility": sum(
                1
                for test in approved_only
                if (
                    test.type == "Compatibility"
                    or test.type == "Cross-Browser"
                    or test.type == "Cross-Device"
                    or test.type == "Responsive"
                )
            ),

            "critical": sum(
                1
                for test in approved_only
                if test.priority == "Critical"
            ),

            "high": sum(
                1
                for test in approved_only
                if test.priority == "High"
            ),

            "medium": sum(
                1
                for test in approved_only
                if test.priority == "Medium"
            ),

            "low": sum(
                1
                for test in approved_only
                if test.priority == "Low"
            )
        }
    )

    # ========================================================
    # STEP 5 — Return Validated Suite
    # ========================================================

    return ValidatedTestSuite(
        test_cases=approved_tests,
        validation_issues=validation_issues,
        duplicates_removed=len(duplicates),
        coverage=coverage
    )