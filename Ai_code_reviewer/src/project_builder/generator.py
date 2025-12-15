from typing import Dict
from src.llm_reviewer import LLMCodeReviewer


class ProjectCodeGenerator:
    """
    Generates Python project files based on:
    - Project blueprint
    - Planned file responsibilities
    - Interaction mode (CLI / GUI)
    """

    def __init__(self, api_key: str):
        self.llm = LLMCodeReviewer(api_key)

    # ==================================================
    # MAIN GENERATION METHOD
    # ==================================================
    def generate_project_code(
        self,
        blueprint: Dict,
        file_plan: Dict[str, str]
    ) -> Dict[str, str]:

        interaction_mode = blueprint.get("interaction_mode", "gui")
        generated_files: Dict[str, str] = {}

        for filename, responsibility in file_plan.items():

            if filename.lower() == "readme.md":
                content = self._generate_readme(blueprint)

            elif filename.lower() == "requirements.txt":
                content = self._generate_requirements(blueprint)

            elif filename in ("main.py", "app.py"):
                if interaction_mode == "cli":
                    content = self._generate_cli_entry(blueprint)
                else:
                    content = self._generate_gui_entry(blueprint)

            else:
                content = self._generate_generic_file(
                    blueprint, filename, responsibility
                )

            generated_files[filename] = content.strip() + "\n"

        return generated_files

    # ==================================================
    # README GENERATION
    # ==================================================
    def _generate_readme(self, blueprint: Dict) -> str:
        project_name = blueprint.get("project_name", "project")
        description = blueprint.get("description", "")
        features = blueprint.get("features", [])
        mode = blueprint.get("interaction_mode", "gui")

        run_cmd = (
            "python main.py"
            if mode == "cli"
            else "streamlit run app.py"
        )

        deps_section = (
            "Install dependencies:\npip install -r requirements.txt\n\n"
            if mode == "gui"
            else ""
        )

        return f"""
# {project_name}

## Description
{description}

## Features
""" + "\n".join(f"- {f}" for f in features) + f"""

## How to Run

1. Extract the ZIP file.
2. Open a terminal inside the project folder.
{deps_section}3. Run the project using:

{run_cmd}

## Notes
- This project was generated automatically.
- Review the code before running.
"""

    # ==================================================
    # REQUIREMENTS GENERATION (AUTO)
    # ==================================================
    def _generate_requirements(self, blueprint: Dict) -> str:
        """
        Generate requirements.txt only when needed.
        """
        interaction_mode = blueprint.get("interaction_mode", "gui")

        if interaction_mode == "gui":
            return "streamlit\n"

        return ""

    # ==================================================
    # CLI ENTRY FILE
    # ==================================================
    def _generate_cli_entry(self, blueprint: Dict) -> str:
        prompt = f"""
Generate a Python CLI application entry file.

Project description:
{blueprint.get("description")}

Features:
{", ".join(blueprint.get("features", []))}

Requirements:
- Use argparse
- Provide subcommands for features
- Call functions from core.py
- Print clear messages
- Do NOT include markdown
"""

        return self.llm.raw_completion(prompt)

    # ==================================================
    # GUI ENTRY FILE (STREAMLIT)
    # ==================================================
    def _generate_gui_entry(self, blueprint: Dict) -> str:
        prompt = f"""
Generate a Streamlit-based Python GUI application.

Project description:
{blueprint.get("description")}

Features:
{", ".join(blueprint.get("features", []))}

Requirements:
- Use streamlit
- Simple and clean UI
- Buttons / inputs for features
- Display outputs clearly
- Do NOT include markdown
"""

        return self.llm.raw_completion(prompt)

    # ==================================================
    # GENERIC FILE GENERATOR
    # ==================================================
    def _generate_generic_file(
        self,
        blueprint: Dict,
        filename: str,
        responsibility: str
    ) -> str:
        prompt = f"""
Generate Python code for the following file.

File name: {filename}
Responsibility: {responsibility}

Project description:
{blueprint.get("description")}

Features:
{", ".join(blueprint.get("features", []))}

Rules:
- Python only
- Modular and clean
- Follow best practices
- Do NOT include markdown
"""

        return self.llm.raw_completion(prompt)
