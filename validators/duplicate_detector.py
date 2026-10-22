from difflib import SequenceMatcher
from typing import List, Tuple

from models.schemas import FinalTestCase


SIMILARITY_THRESHOLD = 0.85


def normalize_text(text: str) -> str:

    return (
        text.lower()
        .strip()
        .replace("-", " ")
        .replace("_", " ")
    )


def calculate_similarity(
    first: str,
    second: str
) -> float:

    first = normalize_text(first)
    second = normalize_text(second)

    return SequenceMatcher(
        None,
        first,
        second
    ).ratio()


def find_duplicate_tests(
    test_cases: List[FinalTestCase]
) -> Tuple[
    List[FinalTestCase],
    List[tuple]
]:

    unique_tests = []

    duplicates = []

    seen_ids = set()

    for current_test in test_cases:

        # ----------------------------------------------------
        # Exact duplicate ID
        # ----------------------------------------------------

        if current_test.test_id in seen_ids:

            duplicates.append(
                (
                    current_test.test_id,
                    current_test.test_id,
                    "Duplicate test ID"
                )
            )

            continue

        # ----------------------------------------------------
        # Semantic duplicate detection
        # ----------------------------------------------------

        duplicate_found = False

        for existing_test in unique_tests:

            title_similarity = calculate_similarity(
                current_test.title,
                existing_test.title
            )

            # Compare title + expected result
            current_combined = (
                current_test.title
                + " "
                + current_test.expected_result
            )

            existing_combined = (
                existing_test.title
                + " "
                + existing_test.expected_result
            )

            combined_similarity = calculate_similarity(
                current_combined,
                existing_combined
            )

            if (
                title_similarity
                >= SIMILARITY_THRESHOLD
                and
                combined_similarity
                >= SIMILARITY_THRESHOLD
            ):

                duplicates.append(
                    (
                        current_test.test_id,
                        existing_test.test_id,
                        (
                            "Semantic duplicate "
                            f"(similarity: "
                            f"{combined_similarity:.2f})"
                        )
                    )
                )

                duplicate_found = True

                break

        if duplicate_found:

            continue

        unique_tests.append(
            current_test
        )

        seen_ids.add(
            current_test.test_id
        )

    return unique_tests, duplicates