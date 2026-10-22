import json

from models.schemas import ValidatedTestSuite


def create_json_report(
    validated_suite: ValidatedTestSuite
):

    data = validated_suite.model_dump()

    return json.dumps(
        data,
        indent=4
    )
