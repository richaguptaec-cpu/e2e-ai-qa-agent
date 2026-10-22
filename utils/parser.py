import json


def parse_json_response(response_text: str):

    text = response_text.strip()

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"AI returned invalid JSON: {exc}"
        ) from exc