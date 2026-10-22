from agents.base_agent import BaseAgent
from models.schemas import TestCaseResponse
from prompts.functional_prompt import FUNCTIONAL_PROMPT

class FunctionalAgent(BaseAgent):

    def generate(
        self,
        user_story,
        acceptance_criteria,
        selected_suites=None
    ):
        """
        Generate functional test cases based on the
        functional test suites selected by the user.

        Supported suites:
            - positive
            - negative
            - edge
        """

        # --------------------------------------------------
        # Default behaviour
        # --------------------------------------------------

        if selected_suites is None:
            selected_suites = [
                "positive",
                "negative",
                "edge"
            ]

        # --------------------------------------------------
        # Validate functional suite IDs
        # --------------------------------------------------

        valid_suites = {
            "positive",
            "negative",
            "edge"
        }

        invalid_suites = [
            suite
            for suite in selected_suites
            if suite not in valid_suites
        ]

        if invalid_suites:

            raise ValueError(
                "Invalid functional test suite(s): "
                + ", ".join(invalid_suites)
            )

        # --------------------------------------------------
        # Remove duplicates while preserving order
        # --------------------------------------------------

        selected_suites = list(
            dict.fromkeys(selected_suites)
        )

        # --------------------------------------------------
        # Convert suite IDs into readable names
        # --------------------------------------------------

        suite_names = {
            "positive": "Positive Cases",
            "negative": "Negative Cases",
            "edge": "Edge Cases"
        }

        selected_suite_names = [
            suite_names[suite]
            for suite in selected_suites
        ]

        selected_suite_text = ", ".join(
            selected_suite_names
        )

        # --------------------------------------------------
        # Build AI prompt
        # --------------------------------------------------

        prompt = FUNCTIONAL_PROMPT.format(
            user_story=user_story,
            acceptance_criteria=acceptance_criteria,
            selected_suites=selected_suite_text
        )

        # --------------------------------------------------
        # Generate structured JSON response
        # --------------------------------------------------

        data = self.ask_json(prompt)

        # --------------------------------------------------
        # Validate generated response
        # --------------------------------------------------

        result = TestCaseResponse.model_validate(
            data
        )

        return result