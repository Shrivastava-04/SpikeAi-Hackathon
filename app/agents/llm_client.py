import json
import re
import os
from openai import OpenAI
from app.agents.llm_prompt import SEO_SYSTEM_PROMPT, SYSTEM_PROMPT
from app.agents.seo_plan import SEOExecutionPlan

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key =os.getenv("LLM_API_KEY"),
            base_url = os.getenv("LLM_BASE_URL")
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
    

    def generate_seo_plan(self, user_query: str) -> SEOExecutionPlan:
        response = self.client.chat.completions.create(
            model="gemini-2.5-pro",
            messages=[
                {"role": "system", "content": SEO_SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
        )

        raw_content = response.choices[0].message.content

        if not raw_content or not raw_content.strip():
            raise ValueError("LLM returned empty response")

        # Remove markdown code fences if present
        cleaned = re.sub(r"```json|```", "", raw_content).strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON from LLM. Raw output was: {raw_content}"
            ) from e

        return SEOExecutionPlan(**data)