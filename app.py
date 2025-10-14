import streamlit as st
import os
import warnings
import sys
import io
import re
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

warnings.filterwarnings("ignore")
load_dotenv()
os.environ["OPENAI_MODEL_NAME"] = "gpt-4"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------- Page Setup ----------------
st.set_page_config(page_title="🤖 Multi-Agent Blog Creator", layout="wide")

st.markdown("<h1 style='text-align:center;'>🤖 Multi-Agent Blog Creator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Watch CrewAI agents (Planner → Writer → Editor) collaborate live!</p>", unsafe_allow_html=True)

topic = st.text_input("🧩 Enter Blog Topic", placeholder="e.g. Attention Mechanism in Deep Learning")
generate_button = st.button("🚀 Generate Blog")

# ---------------- CSS for Scrollable Logs ----------------
st.markdown("""
<style>
.scrollable-log {
    height: 400px;
    overflow-y: auto;
    background-color: #0e1117;
    color: #00ff91;
    border: 1px solid #333;
    padding: 10px;
    border-radius: 8px;
    font-family: monospace;
    font-size: 0.9rem;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Log Cleaning ----------------
ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')

def clean_log(text: str):
    """Remove ANSI color codes and normalize line breaks."""
    text = ansi_escape.sub('', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ---------------- Agent and Task Setup ----------------
def get_agents():
    planner_agent = Agent(
        role="Content Planner",
        goal="Create detailed and factually accurate plans for {topic}.",
        backstory="Expert at planning engaging, structured, and SEO-optimized blogs.",
        allow_delegation=False,
        verbose=True,
    )

    writer_agent = Agent(
        role="Content Writer",
        goal="Write a detailed, accessible, and engaging blog post about {topic}.",
        backstory="Expert in crafting clear and impactful blog posts.",
        allow_delegation=False,
        verbose=True,
    )

    editor_agent = Agent(
        role="Editor",
        goal="Edit the blog to ensure clarity, coherence, and correctness.",
        backstory="Experienced blog editor who ensures a polished final product.",
        allow_delegation=False,
        verbose=True,
    )

    return planner_agent, writer_agent, editor_agent


def get_tasks(planner_agent, writer_agent, editor_agent):
    plan_task = Task(
        description="Create a comprehensive blog content plan for {topic}.",
        expected_output="Content plan with outline, audience analysis, SEO keywords, and resources.",
        agent=planner_agent,
    )

    write_task = Task(
        description="Use the content plan to write a detailed blog post about {topic}.",
        expected_output="A complete blog post in markdown format, with 2–3 paragraphs per section.",
        agent=writer_agent,
    )

    edit_task = Task(
        description="Edit the blog for grammar, flow, and alignment with the content plan.",
        expected_output="A final, polished markdown blog post ready for publishing.",
        agent=editor_agent,
    )

    return plan_task, write_task, edit_task


# ---------------- Main Execution ----------------
if generate_button:
    if not topic.strip():
        st.warning("⚠️ Please enter a topic before generating.")
    else:
        st.markdown("### 🧠 Live CrewAI Execution Logs")

        # Scrollable log area container
        log_container = st.empty()

        # Custom Stream handler
        class StreamToUI(io.StringIO):
            def __init__(self, container):
                super().__init__()
                self.container = container
                self.buffer = ""

            def write(self, message):
                clean_msg = clean_log(message)
                if clean_msg:
                    self.buffer += clean_msg + "\n"
                    # Render scrollable div (HTML-based, styled)
                    self.container.markdown(
                        f"<div class='scrollable-log'>{self.buffer[-8000:]}</div>",
                        unsafe_allow_html=True
                    )
                return len(message)

        # Redirect stdout to custom UI stream
        stream = StreamToUI(log_container)
        old_stdout = sys.stdout
        sys.stdout = stream

        try:
            planner_agent, writer_agent, editor_agent = get_agents()
            plan_task, write_task, edit_task = get_tasks(planner_agent, writer_agent, editor_agent)

            crew = Crew(
                agents=[planner_agent, writer_agent, editor_agent],
                tasks=[plan_task, write_task, edit_task],
                verbose=True
            )

            with st.spinner("🧩 Agents collaborating..."):
                results = crew.kickoff({"topic": topic})

        finally:
            sys.stdout = old_stdout  # Restore normal stdout

        st.success("✅ Agents finished working!")

        # ---------------- Final Result ----------------
        st.markdown("## 📝 Final Blog Post")
        st.markdown(results)

        with st.expander("📄 View Raw Markdown"):
            st.code(results, language="markdown")
