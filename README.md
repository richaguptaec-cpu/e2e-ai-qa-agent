# Intelligent QA Agent: Test Design to Automation by Richa Gupta 🧪🤖

An AI-assisted quality engineering workspace that turns user stories and acceptance criteria into structured, reviewable test suites—and can help translate approved scenarios into Playwright/Pytest automation. Built with Python and Streamlit, the project combines AI-assisted test design with deterministic validation so generated test cases are easier to inspect, score, export, and refine.

> **Project goal:** demonstrate a practical shift-left QA workflow—from requirements analysis to test design, quality checks, exportable test assets, and human-reviewed automation code.

---

## 🚀 Key Engineering Capabilities

### 📝 Requirements-to-Test Generation
- **Acceptance criteria support:** provide a user story and use the app's acceptance-criteria workflow to structure the expected behavior.
- **Selectable test suites:** generate the suites you need rather than forcing every category into a single run.
- **Structured test cases:** organize generated scenarios into consistent fields for review and export.

### 🧪 Specialized QA Coverage
The application is designed around focused test perspectives, including:

- **Positive cases:** expected behavior and successful user journeys.
- **Negative cases:** invalid input, validation failures, and error handling.
- **Edge cases:** boundary values, unusual combinations, and exceptional conditions.
- **Security cases:** security-focused checks such as injection and authorization scenarios, where applicable to the story.
- **Session cases:** session behavior and authentication-related conditions.
- **Performance and network cases:** latency, timeouts, and degraded-network behavior.
- **Accessibility cases:** checks for accessible interactions and content.
- **Compatibility cases:** browser, device, and concurrent-session considerations.

### ✅ Deterministic Quality Checks
- Validate generated test-case structure against defined schemas.
- Detect duplicate or overlapping cases where supported by the validation logic.
- Calculate a test-quality score to help review the completeness of generated output.
- Keep generated cases visible for human review instead of treating AI output as automatically approved.

### 📤 Exportable Test Assets
Export generated test cases for downstream use, including supported **Excel, JSON, and CSV** formats. These files can be reviewed, refined, or adapted for a team's test-management workflow.

### 🤖 Automation Agent (Human-in-the-Loop)
- Generate Playwright/Pytest code for the supported SauceDemo workflow.
- Review the generated code before execution.
- Keep code generation separate from test-case creation so the workflow can be extended without coupling every stage together.

---

## 🏗️ Architecture & Workflow

The application follows a modular agent workflow: requirements and suite selection feed specialized generation components; a validation/reporting stage checks the resulting cases; and the UI presents results for review, export, or automation-code generation.

### System Flow

```text
                 [ User Story / Requirements ]
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     Streamlit UI         │
                 │ Story + AC + Suite Select│
                 └──────────────────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Acceptance Criteria Flow │
                 └──────────────────────────┘
                              │
                              ▼
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
   ┌────────────────────┐              ┌────────────────────┐
   │ Specialized QA     │              │ Specialized QA     │
   │ Agents / Test Types│              │ Agents / Test Types│
   └────────────────────┘              └────────────────────┘
            └─────────────────┬─────────────────┘
                              ▼
                 ┌──────────────────────────┐
                 │ Schema & Quality Checks  │
                 │ Validation / Duplicates  │
                 └──────────────────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Results + Quality Report │
                 └──────────────────────────┘
                       │             │
                       ▼             ▼
                 [ Excel/JSON/CSV ] [ Automation Agent ]
                                            │
                                            ▼
                                  [ Review Playwright Code ]
                                            │
                                            ▼
                                    [ Execute if approved ]
```

### Modular Components

The codebase is organized around agent responsibilities. Names may vary slightly as the implementation evolves; the core responsibilities include:

| Component | Responsibility |
|---|---|
| Acceptance Agent | Extracts or helps structure acceptance criteria from a user story. |
| QA suite agents | Generate cases for the selected test perspectives, such as positive, security, session, performance, accessibility, and compatibility. |
| Validation / quality logic | Checks schema consistency, duplicate cases, and test-case quality. |
| Report Agent | Prepares results for display and export. |
| Automation Agent | Produces Playwright/Pytest code for the supported automation workflow, with review before execution. |

---

## 🛠️ Tech Stack

- **Language:** Python
- **Application UI:** Streamlit
- **LLM Orchestration:** google-genai SDK (Gemini 2.5 Flash model via Google AI Studio free tier)
- **Data models and validation:** Pydantic (where used by the project)
- **Test automation:** Playwright + Pytest for generated automation workflows
- **Test data exports:** Excel, JSON, and CSV
- **AI provider:** configured through the project's environment/settings; check the implementation and `.env.example` for the required provider and variable names

> Dependency versions and the exact AI provider should be taken from the repository's `requirements.txt` and configuration files rather than assumed from this overview.

---

## 💻 Local Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/richaguptaec-cpu/e2e-ai-qa-agent.git
cd e2e-ai-qa-agent
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If the repository includes `requirements.txt`, use:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If there is no `requirements.txt` yet, create one from the dependencies actually imported by the application before sharing the project with others.

### 4. Configure environment variables

Create a local `.env` file if the app requires API credentials. Use the variable names expected by the code or an existing `.env.example` file:

```text
# Example only — use the exact variable name required by your configured AI provider
AI_API_KEY=replace_with_your_api_key
```

**Security note:** keep `.env` out of Git using `.gitignore`. Never commit real API keys or credentials. If a key has already been committed, revoke it and create a replacement.

### 5. Run the Streamlit application

If the entry-point file is `app.py`:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

> If your repository uses a different entry-point or configuration file, follow the actual project structure and update this command accordingly.

---

## 🧭 Typical User Workflow

1. Enter a user story or requirement.
2. Generate or provide acceptance criteria.
3. Select the test suite or suites needed for the requirement.
4. Generate test cases and inspect the results.
5. Review validation feedback, duplicate detection, and the quality score.
6. Export the cases to a supported file format.
7. Where supported, ask the Automation Agent to generate Playwright/Pytest code for the SauceDemo flow.
8. Review the generated code and configuration before running it.

---

## 🔐 Responsible Use & Limitations

- AI-generated test cases and automation code are **drafts**, not proof of correctness. Review them against the requirement and application behavior.
- Generated coverage depends on the quality and completeness of the user story and acceptance criteria.
- Security scenarios generated by the app are test ideas; they do not replace a formal security assessment or authorization to test a system.
- Keep API credentials and any sensitive user or application data out of prompts, logs, screenshots, and committed files.
- Automation generation and execution should remain separate review steps, particularly when code interacts with real systems.

---

## 🗺️ Roadmap

Potential future enhancements, depending on project priorities:

- [ ] Expand automation generation to additional test types and reusable framework patterns.
- [ ] Add richer traceability from user story → acceptance criteria → test case → automation script.
- [ ] Integrate with test-management tools such as Jira/Xray or similar systems.
- [ ] Add CI execution, test-result ingestion, and trend reporting.
- [ ] Improve test-quality scoring with configurable rules and explainable feedback.
- [ ] Add more sample stories and end-to-end demonstrations.

---

## 🖼️ Application Preview

<img width="561" height="186" alt="image" src="https://github.com/user-attachments/assets/a3c32930-d0af-4bf3-a646-5c0892974a6f" />

### 1. Requirements and suite selection

<img width="705" height="311" alt="image" src="https://github.com/user-attachments/assets/98f2f3b6-8306-4f2b-b5e0-4acc3b24fa16" />

### 2. Generated test cases and quality report

<img width="899" height="557" alt="image" src="https://github.com/user-attachments/assets/e05a2e69-2351-4ccc-9362-80f5aefa08be" />

### 4. Generate Acceptance Criteria

<img width="1104" height="235" alt="image" src="https://github.com/user-attachments/assets/62f36745-d3f1-4dc4-acaf-a3a2aa8427b4" />

### 5. Test Generation Summary

<img width="1027" height="586" alt="image" src="https://github.com/user-attachments/assets/c2e247e2-4a64-43bd-a6b7-2d4d495a4af7" />

### 3. Exported test assets

<img width="1151" height="395" alt="image" src="https://github.com/user-attachments/assets/1cde86b7-a19b-4fcb-bdae-769e45fd878d" />

### 4. Automation code generation

<img width="448" height="595" alt="image" src="https://github.com/user-attachments/assets/4498d610-4cd9-4436-bc51-bde1256e1294" />

```markdown

```

---

## 📁 Suggested Repository Structure

Your actual layout may differ; adjust this example to match the files committed to GitHub.

```text
e2e-ai-qa-agent/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── agents/
│   ├── acceptance_agent.py
│   ├── functional_agent.py
│   ├── security_agent.py
│   ├── session_agent.py
│   ├── performance_agent.py
│   ├── accessibility_agent.py
│   ├── compatibility_agent.py
│   ├── report_agent.py
│   └── automation_agent.py
├── schemas/
│   └── ...
├── tests/
│   └── ...
└── docs/
    └── images/
```

---

## 👩‍💻 About

Built as a portfolio project exploring how AI-assisted test design, deterministic validation, and human-reviewed automation can support modern Quality Engineering workflows.

**Author:** Richa Gupta  
**GitHub:** [richaguptaec-cpu](https://github.com/richaguptaec-cpu)

---

## ⭐ Feedback

Suggestions, issues, and improvement ideas are welcome. If you find the project useful, consider starring the repository.
