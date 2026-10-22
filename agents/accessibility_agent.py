from agents.base_agent import BaseAgent
from models.schemas import TestCaseResponse
from prompts.accessibility_prompt import ACCESSIBILITY_PROMPT

class AccessibilityAgent(BaseAgent):

    def generate(
        self,
        user_story,
        acceptance_criteria,
        selected_suites=None
    ):
        """
        Generate accessibility test cases based on
        the accessibility test suites selected by the user.

        Supported suites:
            - accessibility
        """

        # --------------------------------------------------
        # Default behaviour
        # --------------------------------------------------

        if selected_suites is None:
            selected_suites = [
                "accessibility"
            ]

        # --------------------------------------------------
        # Validate accessibility suite IDs
        # --------------------------------------------------

        valid_suites = {
            "accessibility"
        }

        invalid_suites = [
            suite
            for suite in selected_suites
            if suite not in valid_suites
        ]

        if invalid_suites:
            raise ValueError(
                "Invalid accessibility test suite(s): "
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
            "accessibility": "Accessibility"
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

        prompt = ACCESSIBILITY_PROMPT.format(
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