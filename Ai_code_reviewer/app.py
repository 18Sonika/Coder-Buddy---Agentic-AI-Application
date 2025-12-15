import streamlit as st
from datetime import datetime
import re

from src.analyzer import CodeAnalyzer
from src.rules import CodeReviewRules
from src.rewriter import CodeRewriter
from src.llm_reviewer import LLMCodeReviewer

from src.project_builder.blueprint import ProjectBlueprintGenerator
from src.project_builder.planner import ProjectPlanner
from src.project_builder.generator import ProjectCodeGenerator
from src.project_builder.formatter import ProjectFormatter
from src.project_builder.zipper import ProjectZipper

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Coder Buddy - Agentic AI Application",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================
if "review_history" not in st.session_state:
    st.session_state.review_history = []

if "code_gen_history" not in st.session_state:
    st.session_state.code_gen_history = []

if "project_build_history" not in st.session_state:
    st.session_state.project_build_history = []

# ==================================================
# HELPER FUNCTIONS
# ==================================================
def is_python_request(text: str) -> bool:
    """
    Word-boundary safe Python-only validation.
    """
    text = text.lower()
    non_python_languages = [
        "c program", "c language", "c++",
        "java", "javascript", "js",
        "php", "ruby",
        "go language", "golang",
        "rust", "kotlin", "swift"
    ]
    for lang in non_python_languages:
        if re.search(rf"\b{re.escape(lang)}\b", text):
            return False
    return True


def calculate_quality_score(analysis, feedback):
    score = 100
    score -= sum(1 for f in feedback if f.startswith("❌")) * 20
    score -= sum(1 for f in feedback if f.startswith("⚠️")) * 10
    score -= sum(1 for f in feedback if f.startswith("ℹ️")) * 5
    score -= analysis["loops"] * 5
    return max(score, 0)

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("🔐 LLM Configuration")
api_key = st.sidebar.text_input("Enter LLM API Key", type="password")

st.sidebar.markdown("---")

st.sidebar.subheader("🧾 Code Review History")
if st.session_state.review_history:
    for h in st.session_state.review_history:
        st.sidebar.write(f"{h['time']} → {h['score']}/100")
else:
    st.sidebar.caption("No reviews yet")

st.sidebar.markdown("---")

st.sidebar.subheader("✨ Code Generation History")
if st.session_state.code_gen_history:
    for h in st.session_state.code_gen_history:
        st.sidebar.write(f"{h['time']} → {h['prompt'][:30]}...")
else:
    st.sidebar.caption("No generations yet")

st.sidebar.markdown("---")

st.sidebar.subheader("🧩 Mini Project History")
if st.session_state.project_build_history:
    for h in st.session_state.project_build_history:
        st.sidebar.write(
            f"{h['time']} → {h['project']} ({h['mode']})"
        )
else:
    st.sidebar.caption("No projects yet")

# ==================================================
# MAIN UI
# ==================================================
st.title("🤖 Coder Buddy - Agentic AI Application")

mode = st.radio(
    "Select Mode",
    ["🔍 Code Review", "✨ Code Generation", "🧩 Mini Project Builder"],
    horizontal=True
)

st.divider()

# ==================================================
# 🔍 CODE REVIEW MODE
# ==================================================
if mode == "🔍 Code Review":
    st.subheader("🧾 Python Code Review")

    with st.form("review_form"):
        code = st.text_area("Paste Python Code", height=280)
        submit = st.form_submit_button("🔍 Review Code", use_container_width=True)

    if submit and code.strip():
        analyzer = CodeAnalyzer(code)
        analysis = analyzer.run()

        rules = CodeReviewRules(analysis)
        feedback = rules.run_all()

        rewritten = CodeRewriter(code).rewrite()
        score = calculate_quality_score(analysis, feedback)

        st.session_state.review_history.insert(
            0, {"time": datetime.now().strftime("%H:%M:%S"), "score": score}
        )
        st.session_state.review_history = st.session_state.review_history[:5]

        tabs = st.tabs(["🧾 Review", "⭐ Score", "✨ Rewrite", "🤖 LLM"])

        with tabs[0]:
            for f in feedback:
                st.write(f)

        with tabs[1]:
            st.metric("Code Quality Score", f"{score}/100")

        with tabs[2]:
            c1, c2 = st.columns(2)
            c1.code(code, language="python")
            c2.code(rewritten, language="python")

        with tabs[3]:
            if api_key:
                llm = LLMCodeReviewer(api_key)
                st.markdown(llm.review_code(code))
            else:
                st.info("Enter API key to enable LLM review")

# ==================================================
# ✨ CODE GENERATION MODE
# ==================================================
elif mode == "✨ Code Generation":
    st.subheader("✨ Python Code Generator")

    request = st.text_area("Describe the Python code you want", height=180)

    if st.button("✨ Generate Code", use_container_width=True):
        if not request.strip():
            st.warning("Please enter a description.")
        elif not is_python_request(request):
            st.error("Only Python code is supported.")
        elif not api_key:
            st.warning("Please enter API key.")
        else:
            llm = LLMCodeReviewer(api_key)
            code, explanation = llm.generate_code_with_explanation(request)

            st.session_state.code_gen_history.insert(
                0,
                {"time": datetime.now().strftime("%H:%M:%S"), "prompt": request}
            )
            st.session_state.code_gen_history = st.session_state.code_gen_history[:5]

            st.code(code, language="python")
            st.markdown("### 📘 Explanation")
            st.write(explanation)

# ==================================================
# 🧩 MINI PROJECT BUILDER MODE
# ==================================================
else:
    st.subheader("🧩 AI Python Mini Project Builder")

    st.info(
        "🔹 If your prompt contains **CLI / command line**, a CLI project is generated.\n"
        "🔹 Otherwise, a **GUI (Streamlit) project** is generated by default."
    )

    prompt = st.text_area(
        "Describe the Python project you want",
        height=200,
        placeholder="Build a todo app with a simple user interface"
    )

    if st.button("🧩 Build Mini Project", use_container_width=True):

        if not prompt.strip():
            st.warning("Please describe the project.")
        elif not api_key:
            st.warning("Please enter API key.")
        else:
            with st.spinner("Generating project..."):
                blueprint = ProjectBlueprintGenerator(api_key).generate_blueprint(prompt)
                plan = ProjectPlanner().create_plan(blueprint)
                raw_files = ProjectCodeGenerator(api_key).generate_project_code(blueprint, plan)
                files = ProjectFormatter().format_project(raw_files)
                zip_data = ProjectZipper().create_zip(blueprint["project_name"], files)

            st.session_state.project_build_history.insert(
                0,
                {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "project": blueprint["project_name"],
                    "mode": blueprint["interaction_mode"].upper()
                }
            )
            st.session_state.project_build_history = st.session_state.project_build_history[:5]

            st.success("✅ Project generated successfully!")

            st.subheader("▶️ How to Run This Project")
            if blueprint["interaction_mode"] == "cli":
                st.code("python main.py", language="bash")
            else:
                st.code("streamlit run app.py", language="bash")

            st.subheader("📁 Generated Files")
            for name, content in files.items():
                with st.expander(name):
                    if name.endswith(".md"):
                        st.markdown(content)
                    else:
                        st.code(content, language="python")

            st.download_button(
                "⬇️ Download Project (ZIP)",
                zip_data,
                file_name=f"{blueprint['project_name']}.zip",
                mime="application/zip"
            )
