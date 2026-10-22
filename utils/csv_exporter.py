import csv
from io import StringIO

from models.schemas import ValidatedTestSuite


def create_csv_report(
    validated_suite: ValidatedTestSuite
):

    output = StringIO()

    writer = csv.writer(
        output
    )

    writer.writerow([
        "Test ID",
        "Title",
        "Type",
        "Priority",
        "Source Agent",
        "Precondition",
        "Steps",
        "Expected Result",
        "Quality Score",
        "Quality Status",
        "Validation Status"
    ])

    for test in validated_suite.test_cases:

        steps = "\n".join(
            f"{index}. {step}"
            for index, step in enumerate(
                test.steps,
                start=1
            )
        )

        writer.writerow([
            test.test_id,
            test.title,
            test.type,
            test.priority,
            test.source_agent,
            test.precondition,
            steps,
            test.expected_result,
            test.quality_score,
            test.quality_status,
            test.validation_status
        ])

    return output.getvalue()
