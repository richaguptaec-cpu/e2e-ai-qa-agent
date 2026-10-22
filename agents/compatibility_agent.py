from agents.base_agent import BaseAgent
from models.schemas import TestCaseResponse
from prompts.compatibility_prompt import COMPATIBILITY_PROMPT

class CompatibilityAgent(BaseAgent):

    def generate(
        self,
        user_story,
        acceptance_criteria,
        selected_suites=None
    ):
        """
        Generate compatibility test cases based on
        the compatibility test suites selected by the user.

        Supported suites:
            - cross_browser
            - mobile_desktop
        """

        # --------------------------------------------------
        # Default behaviour
        # --------------------------------------------------

        if selected_suites is None:
            selected_suites = [
                "cross_browser",
                "mobile_desktop"
            ]

        # --------------------------------------------------
        # Validate compatibility suite IDs
        # --------------------------------------------------

        valid_suites = {
            "cross_browser",
            "mobile_desktop"
        }

        invalid_suites = [
            suite
            for suite in selected_suites
            if suite not in valid_suites
        ]

        if invalid_suites:
            raise ValueError(
                "Invalid compatibility test suite(s): "
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
            "cross_browser": (
                "Cross-Browser Compatibility"
            ),
            "mobile_desktop": (
                "Mobile/Desktop Compatibility"
            )
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

        prompt = COMPATIBILITY_PROMPT.format(
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