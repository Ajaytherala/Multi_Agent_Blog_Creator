# 🤖 Multi-Agent Blog Creator

An interactive **Streamlit + CrewAI** application that demonstrates how multiple AI agents — a **Planner**, **Writer**, and **Editor** — collaborate in real time to produce a high-quality blog post on any given topic.

This project provides a hands-on demo of **multi-agent collaboration**, showing live logs for each step of the content creation pipeline directly in the browser.

---

## 🚀 Features

✅ **Multi-Agent Workflow**
- **Planner Agent**: Creates a detailed content plan for the given topic.  
- **Writer Agent**: Writes a complete blog post based on the plan.  
- **Editor Agent**: Reviews and refines the blog to ensure clarity and polish.

✅ **Live Execution Logs**
- Real-time, scrollable console output directly in the Streamlit UI.  
- Shows agent execution chains, reasoning, and status updates.  

✅ **Final Output**
- Displays the final, polished blog post in Markdown format.  
- Includes a toggle to view the raw Markdown text for developers or editors.

✅ **Beautiful UI**
- Terminal-style log window with scrolling and syntax highlighting.  
- Minimal, intuitive, and responsive layout designed for demos.

---

## 🧠 Architecture

```text
+--------------------------+
| Streamlit Frontend       |
|  - User enters topic     |
|  - Real-time log display |
|  - Shows final blog      |
+------------+-------------+
             |
             v
+--------------------------+
| CrewAI Backend           |
| 1. Planner Agent         |
| 2. Writer Agent          |
| 3. Editor Agent          |
+--------------------------+
             |
             v
+--------------------------+
| Output: Final Blog (MD)  |
+--------------------------+
