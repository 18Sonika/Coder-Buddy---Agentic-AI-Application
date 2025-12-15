"""
Prompt definitions for the Hybrid AI Python Code Assistant.

This module centralizes all prompt engineering logic to ensure:
- Consistency
- Maintainability
- Easy future enhancements
"""

# ==================================================
# SYSTEM PROMPT (USED ACROSS ALL LLM TASKS)
# ==================================================

SYSTEM_PROMPT = """
You are a senior Python software engineer, code reviewer, and instructor.

General Rules:
- Focus on Python best practices
- Preserve original program logic unless explicitly asked to optimize
- Produce clean, readable, and maintainable code
- Prefer clarity over cleverness
- Be concise and technically accurate
"""

# ==================================================
# CODE REVIEW PROMPT
# ==================================================

def build_review_prompt(code: str) -> str:
    """
    Build prompt for semantic code review and refactoring.
    """
    return f"""
Review the following Python code.

Tasks:
1. Identify code quality issues and bad practices
2. Suggest improvements in readability and structure
3. Provide a cleaner, more Pythonic rewritten version of the code

Constraints:
- Do NOT change the original logic
- Do NOT remove functionality
- Keep suggestions practical and concise

Python Code:
{code}
"""

# ==================================================
# CODE GENERATION (CODE ONLY)
# ==================================================

def build_code_generation_prompt(user_request: str) -> str:
    """
    Build prompt for generating Python code only.
    """
    return f"""
Write clean, correct, and well-documented Python code for the following request.

User Request:
{user_request}

Rules:
- Python only
- Follow best practices
- Add meaningful docstrings
- Use clear variable and function names
- Output ONLY valid Python code
"""

# ==================================================
# CODE GENERATION WITH EXPLANATION
# ==================================================

def build_code_generation_with_explanation_prompt(user_request: str) -> str:
    """
    Build prompt for generating Python code with a short explanation.
    """
    return f"""
Write clean, correct, and well-documented Python code for the following request.

Then provide a short explanation (5–6 lines) describing how the code works.

User Request:
{user_request}

Rules:
- Python only
- Follow best practices
- Add meaningful docstrings
- Do NOT include markdown formatting
- Output format MUST be exactly:

CODE:
<python code>

EXPLANATION:
<short explanation>
"""
