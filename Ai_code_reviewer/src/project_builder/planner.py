from typing import Dict


class ProjectPlanner:
    """
    Converts a project blueprint into a file-level project plan.
    The plan adapts based on interaction mode (CLI or GUI).
    """

    def create_plan(self, blueprint: Dict) -> Dict[str, str]:
        interaction_mode = blueprint.get("interaction_mode", "gui")
        project_type = blueprint.get("project_type", "script")
        features = blueprint.get("features", [])

        plan: Dict[str, str] = {}

        # ---------------------------------------------
        # ENTRY POINT SELECTION
        # ---------------------------------------------
        if interaction_mode == "cli":
            entry_point = "main.py"
            plan[entry_point] = "CLI application entry point"
        else:
            entry_point = "app.py"
            plan[entry_point] = "GUI application entry point"

        # ---------------------------------------------
        # CORE LOGIC (COMMON)
        # ---------------------------------------------
        plan["core.py"] = "Core business logic for project features"

        # ---------------------------------------------
        # STORAGE / PERSISTENCE (CONDITIONAL)
        # ---------------------------------------------
        if any(
            word in f.lower()
            for f in features
            for word in ["store", "file", "save", "persist", "database"]
        ):
            plan["storage.py"] = "Handles data persistence"

        # ---------------------------------------------
        # CLI-SPECIFIC FILES
        # ---------------------------------------------
        if interaction_mode == "cli":
            plan["cli.py"] = "Command-line argument handling and routing"

        # ---------------------------------------------
        # GUI-SPECIFIC FILES
        # ---------------------------------------------
        if interaction_mode == "gui":
            plan["ui.py"] = "User interface logic and layout"

        # ---------------------------------------------
        # DOCUMENTATION
        # ---------------------------------------------
        plan["README.md"] = "Project documentation and usage instructions"
        # ---------------------------------------------
        # DEPENDENCIES (AUTO)
        # ---------------------------------------------
        if interaction_mode == "gui":
         plan["requirements.txt"] = "External dependencies for GUI application"


        return plan
