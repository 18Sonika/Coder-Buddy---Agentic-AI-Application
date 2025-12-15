import ast
from typing import Dict, List, Any


class CodeAnalyzer:
    """
    Analyzes Python source code using AST
    """

    def __init__(self, code: str):
        self.code = code
        self.tree = None
        self.errors: List[str] = []
        self.functions: List[Dict[str, Any]] = []
        self.variables: List[str] = []
        self.imports: List[str] = []
        self.loops: int = 0

    # ---------------- PARSE CODE ----------------
    def parse_code(self) -> bool:
        """
        Parse code and catch syntax errors
        """
        try:
            self.tree = ast.parse(self.code)
            return True
        except SyntaxError as e:
            self.errors.append(
                f"Syntax Error (line {e.lineno}): {e.msg}"
            )
            return False

    # ---------------- ANALYZE AST ----------------
    def analyze(self):
        """
        Walk through AST nodes and collect info
        """
        if not self.tree:
            return

        for node in ast.walk(self.tree):

            # Function definitions
            if isinstance(node, ast.FunctionDef):
                self.functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "length": len(node.body),
                    "has_docstring": ast.get_docstring(node) is not None
                })

            # Variable assignments
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.variables.append(target.id)

            # Import statements
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append(alias.name)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    self.imports.append(node.module)

            # Loops
            if isinstance(node, (ast.For, ast.While)):
                self.loops += 1

    # ---------------- MAIN ENTRY ----------------
    def run(self) -> Dict[str, Any]:
        """
        Run full analysis
        """
        parsed = self.parse_code()
        if parsed:
            self.analyze()

        return {
            "errors": self.errors,
            "functions": self.functions,
            "variables": list(set(self.variables)),
            "imports": list(set(self.imports)),
            "loops": self.loops
        }


# ---------------- QUICK TEST ----------------
if __name__ == "__main__":
    sample_code = """
def add(a, b):
    return a + b

x = 10
for i in range(5):
    print(i)
"""

    analyzer = CodeAnalyzer(sample_code)
    result = analyzer.run()
    print(result)
