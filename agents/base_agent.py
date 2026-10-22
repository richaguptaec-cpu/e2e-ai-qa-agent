from services.gemini_service import GeminiService
from utils.parser import parse_json_response


class BaseAgent:

    def __init__(self):
        self.gemini = GeminiService()

    def ask(self, prompt):
        return self.gemini.generate(prompt)

    def ask_json(self, prompt):

        response = self.ask(prompt)

        return parse_json_response(response)