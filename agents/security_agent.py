from agents.base_agent import BaseAgent
from models.schemas import TestCaseResponse
from prompts.security_prompt import SECURITY_PROMPT

class SecurityAgent(BaseAgent):

    def generate(
        self,
        user_story,
        acceptance_criteria,
        selected_suites=None
    ):
        """
        Generate security test cases based on the
        security test suites selected by the user.

        Supported suites:
            - security
            - sql_injection
        """

        # --------------------------------------------------
        # Default behaviour
        # --------------------------------------------------

        if selected_suites is None:
            selected_suites = [
                "security",
                "sql_injection"
            ]

        # --------------------------------------------------
        # Validate security suite IDs
        # --------------------------------------------------

        valid_suites = {
            "security",
            "sql_injection"
        }

        invalid_suites = [
            suite
            for suite in selected_suites
            if suite not in valid_suites
        ]

        if invalid_suites:
            raise ValueError(
                "Invalid security test suite(s): "
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
            "security": "Security Testing",
            "sql_injection": "SQL Injection"
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

        prompt = SECURITY_PROMPT.format(
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