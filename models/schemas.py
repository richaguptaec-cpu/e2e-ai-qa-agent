from typing import List
from pydantic import BaseModel, Field


# ============================================================
# ACCEPTANCE CRITERIA
# ============================================================

class AcceptanceCriterion(BaseModel):
    id: str
    description: str


class AcceptanceCriteriaResponse(BaseModel):
    acceptance_criteria: List[AcceptanceCriterion]


# ============================================================
# TEST SUITE SELECTION
# ============================================================

class TestSuiteSelection(BaseModel):
    """
    Represents the test suites selected by the user.

    The UI allows users to select specific test suites
    instead of generating the complete QA test suite.

    Example:
        [
            "positive",
            "negative",
            "security",
            "sql_injection"
        ]
    """

    selected_suites: List[str] = Field(
        default_factory=list
    )


# ============================================================
# BASE TEST CASE
# ============================================================

class TestCase(BaseModel):

    test_id: str

    title: str

    type: str

    priority: str

    precondition: str

    steps: List[str]

    expected_result: str


class TestCaseResponse(BaseModel):

    test_cases: List[TestCase]


# ============================================================
# FINAL TEST CASE
# ============================================================

class FinalTestCase(TestCase):

    source_agent: str


# ============================================================
# VALIDATION RESULT
# ============================================================

class ValidationIssue(BaseModel):

    test_id: str

    issue_type: str

    message: str

    severity: str


# ============================================================
# QUALITY INFORMATION
# ============================================================

class QualityResult(BaseModel):

    score: int = Field(
        ge=0,
        le=100
    )

    status: str

    strengths: List[str] = []

    weaknesses: List[str] = []


# ============================================================
# APPROVED TEST CASE
# ============================================================

class ApprovedTestCase(FinalTestCase):

    quality_score: int = Field(
        ge=0,
        le=100
    )

    quality_status: str

    validation_status: str


# ============================================================
# COVERAGE SUMMARY
# ============================================================

class CoverageSummary(BaseModel):

    total_tests: int

    functional: int

    security: int

    session: int

    performance: int

    accessibility: int

    compatibility: int

    critical: int

    high: int

    medium: int

    low: int


# ============================================================
# FINAL TEST SUITE
# ============================================================

class FinalTestSuite(BaseModel):

    test_cases: List[FinalTestCase]

    coverage: CoverageSummary


# ============================================================
# VALIDATED TEST SUITE
# ============================================================

class ValidatedTestSuite(BaseModel):

    test_cases: List[ApprovedTestCase]

    validation_issues: List[ValidationIssue]

    duplicates_removed: int

    coverage: CoverageSummary