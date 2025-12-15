import re
from typing import Dict


class ProjectFormatter:
    """
    Cleans and normalizes LLM-generated project files.
    """

    def format_project(self, files: Dict[str, str]) -> Dict[str, str]:
        """
        Format all files in a generated project.
        """
        formatted = {}

        for filename, content in files.items():
            if filename.lower().endswith(".md"):
                formatted[filename] = self._format_markdown(content)
            else:
                formatted[filename] = self._format_python(content)

        return formatted

    # --------------------------------------------------
    # INTERNAL HELPERS
    # --------------------------------------------------
    def _format_python(self, text: str) -> str:
        """
        Clean Python code output.
        """
        text = self._remove_code_fences(text)
        text = self._remove_explanatory_text(text)
        text = self._normalize_whitespace(text)

        return text.strip() + "\n"

    def _format_markdown(self, text: str) -> str:
        """
        Clean README or markdown files.
        """
        text = self._remove_code_fences(text)
        text = text.strip()

        return text + "\n"

    def _remove_code_fences(self, text: str) -> str:
        """
        Remove markdown code fences.
        """
        text = re.sub(r"```.*?\n", "", text)
        text = text.replace("```", "")
        return text

    def _remove_explanatory_text(self, text: str) -> str:
        """
        Remove common LLM explanatory phrases.
        """
        lines = text.splitlines()
        cleaned = []

        for line in lines:
            if line.lower().startswith((
                "here is",
                "this code",
                "below is",
                "the following"
            )):
                continue
            cleaned.append(line)

        return "\n".join(cleaned)

    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize excessive blank lines.
        """
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text
