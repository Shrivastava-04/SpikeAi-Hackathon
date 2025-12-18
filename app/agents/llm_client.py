import json
import re
from openai import OpenAI
from app.agents.llm_prompt import SYSTEM_PROMPT

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key = "sk-eZBzkrbcflq8m2iss0jV8w",
            base_url = "http://3.110.18.218/v1"
        )

    def _extract_json(self, text: str) -> dict:
        # Remove markdown code blocks if present
        text = text.strip()
        text = re.sub(r"```json|```", "", text).strip()

        # Find first JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in LLM response")

        return json.loads(match.group())
    
    def generate_ga4_plan(self, user_query: str) -> dict:
        response = self.client.chat.completions.create(
            model = "gemini-2.5-pro",
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
        )
        raw_text = response.choices[0].message.content

        return self._extract_json(raw_text)