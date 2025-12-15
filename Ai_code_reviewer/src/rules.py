from typing import Dict, List


class CodeReviewRules:
    """
    Applies code quality rules on analyzed Python code
    """

    def __init__(self, analysis_result: Dict):
        self.analysis = analysis_result
        self.comments: List[str] = []

    # ---------------- RULE: SYNTAX ERRORS ----------------
    def check_syntax_errors(self):
        if self.analysis["errors"]:
            for err in self.analysis["errors"]:
                self.comments.append(f"❌ {err}")

    # ---------------- RULE: LONG FUNCTIONS ----------------
    def check_long_functions(self, max_lines: int = 20):
        for func in self.analysis["functions"]:
            if func["length"] > max_lines:
                self.comments.append(
                    f"⚠️ Function '{func['name']}' is too long "
                    f"({func['length']} lines). Consider splitting it."
                )

    # ---------------- RULE: MISSING DOCSTRINGS ----------------
    def check_missing_docstrings(self):
        for func in self.analysis["functions"]:
            if not func["has_docstring"]:
                self.comments.append(
                    f"ℹ️ Function '{func['name']}' is missing a docstring."
                )

    # ---------------- RULE: TOO MANY LOOPS ----------------
    def check_excessive_loops(self, max_loops: int = 3):
        if self.analysis["loops"] > max_loops:
            self.comments.append(
                f"⚠️ Code contains {self.analysis['loops']} loops. "
                "Consider optimizing nested or repeated loops."
            )

    # ---------------- RULE: VARIABLE NAMING ----------------
    def check_variable_naming(self):
        for var in self.analysis["variables"]:
            if len(var) == 1:
                self.comments.append(
                    f"ℹ️ Variable '{var}' has a very short name. "
                    "Use more descriptive variable names."
                )

    # ---------------- RUN ALL RULES ----------------
    def run_all(self) -> List[str]:
        self.check_syntax_errors()
        self.check_long_functions()
        self.check_missing_docstrings()
        self.check_excessive_loops()
        self.check_variable_naming()

        if not self.comments:
            self.comments.append("✅ No major issues found. Code looks clean!")

        return self.comments


# ---------------- QUICK TEST ----------------
if __name__ == "__main__":
    sample_analysis = {
        "errors": [],
        "functions": [
            {"name": "process", "length": 35, "has_docstring": False}
        ],
        "variables": ["x", "total"],
        "imports": [],
        "loops": 4
    }

    reviewer = CodeReviewRules(sample_analysis)
    feedback = reviewer.run_all()
    for f in feedback:
        print(f)
