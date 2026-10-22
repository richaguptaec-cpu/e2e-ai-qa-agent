from models.schemas import (
    FinalTestCase,
    QualityResult
)


def calculate_quality_score(
    test: FinalTestCase
) -> QualityResult:

    score = 0

    strengths = []

    weaknesses = []

    # ========================================================
    # TITLE
    # ========================================================

    if test.title.strip():

        score += 20

        strengths.append(
            "Clear test title."
        )

    else:

        weaknesses.append(
            "Missing test title."
        )

    # ========================================================
    # PRECONDITION
    # ========================================================

    if test.precondition.strip():

        score += 15

        strengths.append(
            "Precondition is defined."
        )

    else:

        weaknesses.append(
            "Precondition is missing."
        )

    # ========================================================
    # STEPS
    # ========================================================

    if len(test.steps) >= 2:

        score += 25

        strengths.append(
            "Test contains actionable steps."
        )

    elif len(test.steps) == 1:

        score += 15

        weaknesses.append(
            "Test contains only one step."
        )

    else:

        weaknesses.append(
            "Test has no steps."
        )

    # ========================================================
    # EXPECTED RESULT
    # ========================================================

    if test.expected_result.strip():

        score += 20

        strengths.append(
            "Expected result is defined."
        )

    else:

        weaknesses.append(
            "Expected result is missing."
        )

    # ========================================================
    # SPECIFICITY
    # ========================================================

    vague_words = [
        "check",
        "verify something",
        "test it",
        "works correctly",
        "works fine",
        "as expected"
    ]

    title_lower = test.title.lower()

    if not any(
        word in title_lower
        for word in vague_words
    ):

        score += 10

        strengths.append(
            "Test title is reasonably specific."
        )

    else:

        weaknesses.append(
            "Test title may be too vague."
        )

    # ========================================================
    # EXPECTED RESULT SPECIFICITY
    # ========================================================

    vague_result_words = [
        "works correctly",
        "works fine",
        "should work",
        "as expected"
    ]

    result_lower = (
        test.expected_result.lower()
    )

    if not any(
        word in result_lower
        for word in vague_result_words
    ):

        score += 10

        strengths.append(
            "Expected result is reasonably specific."
        )

    else:

        weaknesses.append(
            "Expected result may be too vague."
        )

    # ========================================================
    # QUALITY STATUS
    # ========================================================

    if score >= 85:

        status = "Excellent"

    elif score >= 70:

        status = "Good"

    elif score >= 50:

        status = "Needs Improvement"

    else:

        status = "Poor"

    return QualityResult(
        score=score,
        status=status,
        strengths=strengths,
        weaknesses=weaknesses
    )