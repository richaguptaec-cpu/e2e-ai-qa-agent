from agents.base_agent import BaseAgent
from models.schemas import TestCaseResponse
from prompts.session_prompt import SESSION_PROMPT

class SessionAgent(BaseAgent):

    def generate(
        self,
        user_story,
        acceptance_criteria,
        selected_suites=None
    ):
        """
        Generate session-related test cases based on
        the session test suites selected by the user.

        Supported suites:
            - session
            - concurrent_sessions
        """

        # --------------------------------------------------
        # Default behaviour
        # --------------------------------------------------

        if selected_suites is None:
            selected_suites = [
                "session",
                "concurrent_sessions"
            ]

        # --------------------------------------------------
        # Validate session suite IDs
        # --------------------------------------------------

        valid_suites = {
            "session",
            "concurrent_sessions"
        }

        invalid_suites = [
            suite
            for suite in selected_suites
            if suite not in valid_suites
        ]

        if invalid_suites:
            raise ValueError(
                "Invalid session test suite(s): "
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
            "session": "Session Management",
            "concurrent_sessions": "Concurrent Sessions"
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

        prompt = SESSION_PROMPT.format(
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