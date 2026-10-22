from agents.base_agent import BaseAgent
from models.schemas import AcceptanceCriteriaResponse
from prompts.acceptance_prompt import ACCEPTANCE_PROMPT


class AcceptanceAgent(BaseAgent):

    def generate(self, user_story):

        prompt = ACCEPTANCE_PROMPT.format(
            user_story=user_story
        )

        data = self.ask_json(prompt)

        result = AcceptanceCriteriaResponse.model_validate(data)

        return result