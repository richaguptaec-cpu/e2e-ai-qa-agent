from validators.test_suite_validator import (
validate_test_suite
)

from agents.acceptance_agent import AcceptanceAgent
from agents.functional_agent import FunctionalAgent
from agents.security_agent import SecurityAgent
from agents.session_agent import SessionAgent
from agents.performance_agent import PerformanceAgent
from agents.accessibility_agent import AccessibilityAgent
from agents.compatibility_agent import CompatibilityAgent
from agents.report_agent import ReportAgent

from models.schemas import (
AcceptanceCriteriaResponse,
AcceptanceCriterion
)

from utils.helpers import acceptance_criteria_to_text

class QAOrchestrator:
    """
    Central coordinator for the multi-agent QA system.

    ```
    Responsibilities:
    1. Generate or accept Acceptance Criteria.
    2. Identify the QA test suites selected by the user.
    3. Send requirements only to the required specialist agents.
    4. Collect outputs from the selected specialist agents.
    5. Send generated scenarios to ReportAgent.
    6. Run deterministic QA validation.
    7. Return the consolidated final QA test suite.
    """

    def __init__(self):

        # --------------------------------------------------
        # Initialize all specialist agents
        # --------------------------------------------------

        self.acceptance_agent = AcceptanceAgent()

        self.functional_agent = FunctionalAgent()

        self.security_agent = SecurityAgent()

        self.session_agent = SessionAgent()

        self.performance_agent = PerformanceAgent()

        self.accessibility_agent = AccessibilityAgent()

        self.compatibility_agent = CompatibilityAgent()

        # --------------------------------------------------
        # Initialize final report/consolidation agent
        # --------------------------------------------------

        self.report_agent = ReportAgent()

    def process(
        self,
        user_story,
        option,
        acceptance_text=None,
        selected_suites=None
    ):
        """
        Main orchestration workflow.

        Parameters
        ----------
        user_story : str
            User story entered by the user.

        option : str
            "Generate" if AI should generate acceptance criteria.
            "Enter" if user provided acceptance criteria manually.

        acceptance_text : str, optional
            Manually entered acceptance criteria.

        selected_suites : list[str], optional
            Test suite IDs selected by the user.

        Returns
        -------
        dict
            Results from the selected agents and the final
            consolidated and validated QA test suite.
        """

        # ==================================================
        # STEP 1: Validate User Story
        # ==================================================

        if not user_story or not user_story.strip():

            raise ValueError(
                "User story cannot be empty."
            )

        user_story = user_story.strip()

        # ==================================================
        # STEP 2: Validate Selected Test Suites
        # ==================================================

        if not selected_suites:

            raise ValueError(
                "At least one test suite must be selected."
            )

        # Remove accidental duplicates while preserving
        # the original selection order.

        selected_suites = list(
            dict.fromkeys(selected_suites)
        )

        # ==================================================
        # STEP 3: Validate Suite IDs
        # ==================================================

        valid_suite_ids = {
            "positive",
            "negative",
            "edge",
            "security",
            "sql_injection",
            "session",
            "concurrent_sessions",
            "network_latency",
            "accessibility",
            "cross_browser",
            "mobile_desktop"
        }

        invalid_suites = [
            suite
            for suite in selected_suites
            if suite not in valid_suite_ids
        ]

        if invalid_suites:

            raise ValueError(
                "Invalid test suite selection: "
                + ", ".join(invalid_suites)
            )

        # ==================================================
        # STEP 4: Generate or Parse Acceptance Criteria
        # ==================================================

        if option == "Generate":

            acceptance_result = (
                self.acceptance_agent.generate(
                    user_story
                )
            )

        elif option == "Enter":

            if (
                acceptance_text is None
                or not acceptance_text.strip()
            ):

                raise ValueError(
                    "Acceptance criteria cannot be empty "
                    "when using the Enter option."
                )

            acceptance_result = (
                self._parse_manual_acceptance(
                    acceptance_text
                )
            )

        else:

            raise ValueError(
                "Invalid acceptance criteria option. "
                "Use 'Generate' or 'Enter'."
            )

        # ==================================================
        # STEP 5: Convert Acceptance Criteria to Text
        # ==================================================

        acceptance_for_prompt = (
            acceptance_criteria_to_text(
                acceptance_result
            )
        )

        # ==================================================
        # STEP 6: Initialize Agent Results
        # ==================================================

        functional_result = None
        security_result = None
        session_result = None
        performance_result = None
        accessibility_result = None
        compatibility_result = None

        # ==================================================
        # STEP 7: Functional Testing
        #
        # Handles:
        #   positive
        #   negative
        #   edge
        # ==================================================

        functional_suites = [
            suite
            for suite in selected_suites
            if suite in {
                "positive",
                "negative",
                "edge"
            }
        ]

        if functional_suites:

            functional_result = (
                self.functional_agent.generate(
                    user_story=user_story,
                    acceptance_criteria=acceptance_for_prompt,
                    selected_suites=functional_suites
                )
            )

        # ==================================================
        # STEP 8: Security Testing
        #
        # Handles:
        #   security
        #   sql_injection
        # ==================================================

        security_suites = [
            suite
            for suite in selected_suites
            if suite in {
                "security",
                "sql_injection"
            }
        ]

        if security_suites:

            security_result = (
                self.security_agent.generate(
                    user_story=user_story,
                    acceptance_criteria=acceptance_for_prompt,
                    selected_suites=security_suites
                )
            )

        # ==================================================
        # STEP 9: Session Testing
        #
        # Handles:
        #   session
        #   concurrent_sessions
        # ==================================================

        session_suites = [
            suite
            for suite in selected_suites
            if suite in {
                "session",
                "concurrent_sessions"
            }
        ]

        if session_suites:

            session_result = (
                self.session_agent.generate(
                    user_story=user_story,
                    acceptance_criteria=acceptance_for_prompt,
                    selected_suites=session_suites
                )
            )

        # ==================================================
        # STEP 10: Performance Testing
        #
        # Handles:
        #   network_latency
        # ==================================================

        performance_suites = [
            suite
            for suite in selected_suites
            if suite == "network_latency"
        ]

        if performance_suites:

            performance_result = (
                self.performance_agent.generate(
                    user_story=user_story,
                    acceptance_criteria=acceptance_for_prompt,
                    selected_suites=performance_suites
                )
            )

        # ==================================================
        # STEP 11: Accessibility Testing
        #
        # Handles:
        #   accessibility
        # ==================================================

        accessibility_suites = [
            suite
            for suite in selected_suites
            if suite == "accessibility"
        ]

        if accessibility_suites:

            accessibility_result = (
                self.accessibility_agent.generate(
                    user_story=user_story,
                    acceptance_criteria=acceptance_for_prompt,
                    selected_suites=accessibility_suites
                )
            )

        # ==================================================
        # STEP 12: Compatibility Testing
        #
        # Handles:
        #   cross_browser
        #   mobile_desktop
        # ==================================================

        compatibility_suites = [
            suite
            for suite in selected_suites
            if suite in {
                "cross_browser",
                "mobile_desktop"
            }
        ]

        if compatibility_suites:

            compatibility_result = (
                self.compatibility_agent.generate(
                    user_story=user_story,
                    acceptance_criteria=acceptance_for_prompt,
                    selected_suites=compatibility_suites
                )
            )

        # ==================================================
        # STEP 13: Consolidate Selected Test Cases
        # ==================================================

        final_suite = (
            self.report_agent.generate(
                user_story=user_story,

                acceptance_criteria=acceptance_for_prompt,

                functional=functional_result,

                security=security_result,

                session=session_result,

                performance=performance_result,

                accessibility=accessibility_result,

                compatibility=compatibility_result
            )
        )

        # ==================================================
        # STEP 14: Deterministic QA Validation
        #
        # Includes:
        #   - Test structure validation
        #   - Duplicate detection
        #   - Quality scoring
        #   - Approval / Review status
        #   - Coverage recalculation
        # ==================================================

        validated_suite = validate_test_suite(
            final_suite
        )

        # ==================================================
        # STEP 15: Return Complete QA Analysis
        # ==================================================

        return {
            "acceptance_criteria": acceptance_result,

            "selected_suites": selected_suites,

            "functional": functional_result,

            "security": security_result,

            "session": session_result,

            "performance": performance_result,

            "accessibility": accessibility_result,

            "compatibility": compatibility_result,

            "final_suite": final_suite,

            "validated_suite": validated_suite
        }

    def _parse_manual_acceptance(
        self,
        acceptance_text
    ):
        """
        Convert manually entered acceptance criteria
        into the same Pydantic structure used by the
        AcceptanceAgent.

        Each non-empty line is treated as one criterion.
        """

        lines = [
            line.strip()
            for line in acceptance_text.splitlines()
            if line.strip()
        ]

        criteria = []

        for index, line in enumerate(
            lines,
            start=1
        ):

            criteria.append(
                AcceptanceCriterion(
                    id=f"AC{index:03d}",
                    description=line
                )
            )

        return AcceptanceCriteriaResponse(
            acceptance_criteria=criteria
        )