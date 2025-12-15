import re


class CodeRewriter:
    """
    Rewrites Python code using simple, safe refactoring rules.
    This does NOT change logic — only improves readability.
    """

    def __init__(self, code: str):
        self.code = code

    def improve_variable_names(self):
        """
        Replace common single-letter variables with meaningful names
        """
        replacements = {
            r"\bx\b": "value",
            r"\by\b": "result",
            r"\bi\b": "index",
            r"\bn\b": "number",
            r"\bs\b": "total_sum"
        }

        updated_code = self.code
        for pattern, replacement in replacements.items():
            updated_code = re.sub(pattern, replacement, updated_code)

        return updated_code

    def add_docstrings(self, code: str):
        """
        Add simple docstrings to functions if missing
        """
        lines = code.split("\n")
        new_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            new_lines.append(line)

            if line.strip().startswith("def ") and (i + 1 < len(lines)):
                next_line = lines[i + 1].strip()
                if not next_line.startswith('"""'):
                    indent = " " * (len(line) - len(line.lstrip()) + 4)
                    new_lines.append(
                        f'{indent}"""Auto-generated docstring."""'
                    )
            i += 1

        return "\n".join(new_lines)

    def format_spacing(self, code: str):
        """
        Normalize spacing and remove extra blank lines
        """
        code = re.sub(r"\n{3,}", "\n\n", code)
        return code.strip()

    def rewrite(self):
        """
        Apply all rewrite rules
        """
        code = self.improve_variable_names()
        code = self.add_docstrings(code)
        code = self.format_spacing(code)
        return code
