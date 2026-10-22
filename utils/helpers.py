from models.schemas import AcceptanceCriteriaResponse


def acceptance_criteria_to_text(
    acceptance_response: AcceptanceCriteriaResponse
):

    return "\n".join(
        f"{item.id}: {item.description}"
        for item in acceptance_response.acceptance_criteria
    )