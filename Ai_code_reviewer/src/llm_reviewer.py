from groq import Groq
from src.prompts import (
    SYSTEM_PROMPT,
    build_review_prompt,
    build_code_generation_prompt,
    build_code_generation_with_explanation_prompt
)


class LLMCodeReviewer:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model_name = "openai/gpt-oss-120b"

    # --------------------------------------------------
    # 🔍 CODE REVIEW
    # --------------------------------------------------
    def review_code(self, code: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_review_prompt(code)}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

    # --------------------------------------------------
    # ✨ CODE GENERATION
    # --------------------------------------------------
    def generate_code(self, user_request: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are an expert Python programmer."},
                {"role": "user", "content": build_code_generation_prompt(user_request)}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

    # --------------------------------------------------
    # ✨ CODE + EXPLANATION
    # --------------------------------------------------
    def generate_code_with_explanation(self, user_request: str):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python programmer and teacher."
                },
                {
                    "role": "user",
                    "content": build_code_generation_with_explanation_prompt(user_request)
                }
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        if "EXPLANATION:" in content:
            code_part, explanation_part = content.split("EXPLANATION:", 1)
            code = code_part.replace("CODE:", "").strip()
            explanation = explanation_part.strip()
        else:
            code = content
            explanation = "Explanation not available."

        return code, explanation

    # --------------------------------------------------
    # 🧩 RAW COMPLETION (FOR MINI PROJECT BUILDER)
    # --------------------------------------------------
    def raw_completion(self, prompt: str) -> str:
        """
        Low-level completion method used by:
        - Project Blueprint Generator
        - Project File Generator
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior Python software architect."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()
