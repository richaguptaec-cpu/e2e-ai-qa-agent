from agents.base_agent import BaseAgent
from prompts.automation_prompt import AUTOMATION_PROMPT


class AutomationAgent(BaseAgent):
    """
    Generate Playwright/Pytest automation code from an
    approved test case.

    Generated code must be reviewed before execution.
    """

    def generate(
        self,
        base_url,
        approved_test_case,
        user_story="",
        acceptance_criteria="",
        page_information="Not provided"
    ):
        if not base_url or not base_url.strip():
            raise ValueError(
                "A target website URL is required."
            )

        if not approved_test_case:
            raise ValueError(
                "An approved test case is required."
            )

        prompt = AUTOMATION_PROMPT.format(
            base_url=base_url.strip(),
            user_story=user_story or "Not provided",
            acceptance_criteria=(
                acceptance_criteria or "Not provided"
            ),
            approved_test_case=approved_test_case,
            page_information=(
                page_information or "Not provided"
            )
        )

        data = self.ask_json(prompt)

        if not isinstance(data, dict):
            raise ValueError(
                "The Automation Agent did not return "
                "a valid JSON object."
            )

        required_fields = {
            "filename",
            "test_name",
            "code",
            "assumptions",
            "manual_review_required"
        }

        missing_fields = required_fields - set(data.keys())

        if missing_fields:
            raise ValueError(
                "Automation response is missing fields: "
                + ", ".join(sorted(missing_fields))
            )

        if not isinstance(data["code"], str):
            raise ValueError(
                "The generated code must be a string."
            )

        if not data["code"].strip():
            raise ValueError(
                "The Automation Agent generated empty code."
            )

        return data
