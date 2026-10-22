🧪 AI QA Agent by Richa Gupta
A multi-agent AI Quality Engineering platform that turns user stories into structured, reviewable test scenarios and can generate Playwright/Pytest automation code.

The goal of this project is to explore how AI-assisted workflows can support QA engineers across test analysis, test design, quality checks, reporting, and UI automation.
✨ Key Features
1. User story and acceptance criteria
- Enter a user story and provide acceptance criteria, or use the app's acceptance-criteria workflow where available.
- Use the generated criteria as input to test design.
2. Targeted test-suite generation
Select the test suites you need instead of generating every category at once. Supported categories in the project include:
- Positive cases — expected behaviour for valid inputs and workflows.
- Negative cases — invalid inputs and failure scenarios.
- Edge cases — boundary conditions and unusual combinations.
- Security — security-focused scenarios, including injection-related checks.
- Session — session and authentication-related behaviour.
- Performance / network — latency and network-condition scenarios.
- Accessibility — accessibility-focused checks.
- Compatibility — browser, device, and concurrent-session considerations.
The available categories depend on the current implementation and selected suites.
3. Test-case quality checks
- Validate generated test cases.
- Detect potential duplicate scenarios.
- Review test quality and coverage summaries before using the output.
AI-generated scenarios are suggestions: review them against the product requirements, risk profile, and test environment before execution.
4. Exportable reports
Export generated test cases for further review or test-management workflows in supported formats:
- Excel (.xlsx)
- JSON (.json)
- CSV (.csv)
5. Playwright automation agent
- Select a generated test case for automation.
- Provide the target application URL and any required test credentials.
- Generate Playwright/Pytest code for review.
- Review assumptions and generated code before approving execution.
- Run the approved test and inspect the execution output.
The automation workflow is intended to keep a human review step before running generated code. Use a dedicated test environment and non-production credentials.
🧰 Technology Stack
- Python
- Streamlit — interactive web application
- AI / LLM agents — acceptance-criteria and test-design assistance, according to the configured provider
- Pydantic — structured data validation (project schemas)
- Playwright — browser automation
- Pytest — test execution
- Pandas / Excel tooling — report generation, as used by the project
🗂️ Project Structure
The app imports functionality from modules organized along these lines:
.
├── app.py
├── agents/
│   ├── orchestrator.py
│   ├── automation_agent.py
│   └── ...agent modules
├── automation/
│   ├── test_generator.py
│   └── test_runner.py
├── models/
│   └── schemas.py
├── utils/
│   ├── excel_exporter.py
│   ├── json_exporter.py
│   └── csv_exporter.py
├── requirements.txt
└── README.md
Your actual repository may contain additional modules. Keep the existing package and file names consistent with the imports in app.py.
🚀 Getting Started
Prerequisites
- Python 3.10 or newer (use the version supported by your dependencies)
- pip
- Git
- An API key for the LLM provider configured in your agent implementation, if required
- A browser supported by the installed Playwright version for automation runs
1. Clone the repository
Replace the placeholder below with your GitHub repository URL:
git clone https://github.com/<YOUR-GITHUB-USERNAME>/<YOUR-REPOSITORY-NAME>.git
cd <YOUR-REPOSITORY-NAME>
2. Create and activate a virtual environment
Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
If the repository includes requirements.txt:
python -m pip install --upgrade pip
pip install -r requirements.txt
If requirements.txt is not present yet, create it from the project's actual imports and pinned, tested dependency versions before publishing. Avoid guessing dependency versions.
4. Configure environment variables
Set the API key expected by your configured LLM integration. The exact variable name depends on the provider and the code in this repository.

For local development, use a .env file only if the project loads it, or set the variable in your terminal. For example, in PowerShell:
$env:YOUR_LLM_API_KEY="your-api-key"
Replace YOUR_LLM_API_KEY with the variable name your agent code actually reads.

Security: Never commit API keys, passwords, access tokens, real customer data, or production secrets to GitHub. Add .env and other secret files to .gitignore.
5. Launch the app
From the repository root:
streamlit run app.py
Streamlit will print a local URL in the terminal. Open that URL in your browser.
🧭 Typical Workflow
1. Enter a user story.
2. Add or generate acceptance criteria, depending on the available workflow.
3. Select the test-suite categories relevant to the story.
4. Generate test cases and review validation, coverage, and quality summaries.
5. Export the cases to Excel, JSON, or CSV.
6. Optionally select a case in the automation section, provide a test URL and test credentials, and generate Playwright/Pytest code.
7. Review the code and assumptions carefully before approving execution.
8. Run against a dedicated test environment and inspect the result.
🧪 Running Generated Automation
Generated tests depend on the target application's current UI, test data, and authentication flow. Before execution:
- Confirm the target URL is correct and points to a test environment.
- Use test accounts and non-sensitive data.
- Review locators, assertions, and any generated setup or teardown code.
- Confirm that the test does not perform destructive actions.
- Install the browsers required by Playwright if they are not already installed:
playwright install
Run the generated test through the app's automation workflow or use the appropriate Pytest command for the generated file. The exact command and output path depend on the implementation.
🔐 Security and Responsible Use
- Treat LLM output as a draft, not as a substitute for QA judgement.
- Do not submit confidential user stories or sensitive data to an AI provider unless permitted by your organization's policies.
- Keep secrets in environment variables or an approved secret manager.
- Run generated code only after reviewing it.
- Use isolated, non-production environments for browser automation.
- Validate security test ideas only against systems you own or are explicitly authorized to test.
🛣️ Potential Next Steps
Possible improvements for future iterations:
- Add unit tests and integration tests for the agent workflow.
- Add CI checks for formatting, linting, and tests.
- Add richer test traceability from user story to acceptance criteria to test cases.
- Add reusable prompt templates and configurable model settings.
- Add more detailed execution reports, screenshots, and Playwright traces.
- Integrate with a test-management tool after validating the export workflow.
⚠️ Project Status
This is an evolving project. AI-generated test cases and automation code require human review, and features may change as the implementation develops. Confirm dependencies, required environment variables, and execution commands against the current source before using the project in another environment.
👩‍💻 Author
Richa Gupta

This project demonstrates practical exploration of AI-assisted quality engineering, structured test design, reporting, and Playwright/Pytest automation.