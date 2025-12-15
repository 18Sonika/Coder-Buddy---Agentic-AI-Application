from typing import Dict
import json

from src.llm_reviewer import LLMCodeReviewer


class ProjectBlueprintGenerator:
    """
    Converts a natural language project description into
    a structured Python project blueprint.
    """

    def __init__(self, api_key: str):
        self.llm = LLMCodeReviewer(api_key)

    # --------------------------------------------------
    # 🔎 INTERACTION MODE DETECTION
    # --------------------------------------------------
    def _detect_interaction_mode(self, prompt: str) -> str:
        """
        Detect whether the project should be CLI or GUI based
        on user prompt keywords.
        """
        prompt = prompt.lower()

        cli_keywords = ["cli", "command line", "terminal"]
        gui_keywords = ["gui", "ui", "interface", "dashboard", "app"]

        if any(word in prompt for word in cli_keywords):
            return "cli"

        if any(word in prompt for word in gui_keywords):
            return "gui"

        # Default behavior (more user-friendly)
        return "gui"

    # --------------------------------------------------
    # 🧩 BLUEPRINT GENERATION
    # --------------------------------------------------
    def generate_blueprint(self, user_prompt: str) -> Dict:
        interaction_mode = self._detect_interaction_mode(user_prompt)

        prompt = f"""
You are a senior Python software architect.

Analyze the following project request and extract a structured
project blueprint.

Rules:
- Python projects only
- Do NOT generate code
- Do NOT add assumptions
- Use snake_case for names
- Be concise and clear

Return output STRICTLY in valid JSON format:

{{
  "project_name": "<short_snake_case_name>",
  "project_type": "<script | web | gui | library>",
  "interaction_mode": "{interaction_mode}",
  "description": "<1-2 line summary>",
  "features": [
    "<feature 1>",
    "<feature 2>",
    "<feature 3>"
  ],
  "entry_point": "<main python file name>"
}}

Project Request:
\"\"\"{user_prompt}\"\"\"
"""

        response_text = self.llm.raw_completion(prompt)
        return self._parse_response(response_text)

    # --------------------------------------------------
    # 🛡️ SAFE JSON PARSING
    # --------------------------------------------------
    def _parse_response(self, text: str) -> Dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(
                "Failed to generate a valid project blueprint. "
                "Please rephrase your project description."
            )
