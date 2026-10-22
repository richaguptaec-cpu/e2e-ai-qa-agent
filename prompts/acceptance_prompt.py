ACCEPTANCE_PROMPT = """
You are a Senior Business Analyst and QA Architect.

Your task is to analyze the user story and generate
comprehensive acceptance criteria.

USER STORY:
{user_story}

Requirements:

1. Identify the main business behavior.
2. Identify successful behavior.
3. Identify validation rules.
4. Identify invalid input behavior.
5. Identify error handling.
6. Identify important business rules.
7. Identify authentication or authorization requirements
   if applicable.
8. Do not invent highly specific business rules that are
   not reasonably implied by the user story.

Return ONLY valid JSON.

Required JSON format:

{{
    "acceptance_criteria": [
        {{
            "id": "AC001",
            "description": "..."
        }}
    ]
}}

Do not include markdown.
Do not include explanations outside the JSON.
"""