# 🎓 Study Buddy Agent

An AI-powered study assistant built with LangChain, LangGraph, and Groq. Give it any topic and a learning goal — it searches the web, builds a structured lesson plan, teaches you lesson by lesson, quizzes you after each one, and gives you a final score report.

## Features

- Structured lesson plans (3–5 lessons) generated from real web search results
- Quiz after every lesson with instant feedback
- Progress tracking across the full session
- Fully free stack — no paid APIs required
- Clean Streamlit chat UI with live sidebar progress

## Tech Stack

| Component  | Library                                      |
| ---------- | -------------------------------------------- |
| Agent      | `langchain.agents.create_agent`              |
| LLM        | `langchain-groq` — `llama-3.3-70b-versatile` |
| Memory     | `langgraph.checkpoint.memory.InMemorySaver`  |
| Web Search | `ddgs`                                       |
| UI         | `streamlit`                                  |

## Project Structure

```
study-buddy-agent/
├── agent/
│   ├── __init__.py
│   ├── agent.py        # Agent setup (LLM, checkpointer, tools, system prompt)
│   └── tools.py        # web_search, track_progress, reset_progress
├── app.py              # Streamlit UI
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/AbdelazizAushar/study-buddy-agent.git
cd study-buddy-agent
```

**2. Create and activate a virtual environment**

```bash
conda create -n study-buddy python=3.11
conda activate study-buddy
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up your environment variables**

```bash
cp .env.example .env
```

Then add your Groq API key to `.env`:

```
GROQ_API_KEY=your_key_here
```

Get a free key at [console.groq.com](https://console.groq.com)

**5. Run the app**

```bash
streamlit run app.py
```

## How It Works

1. Enter a topic and your learning goal
2. The agent searches the web for accurate, up-to-date information
3. It builds a 3–5 lesson plan and presents it to you
4. After each lesson it quizzes you with 1–2 questions
5. Your score is tracked in the sidebar in real time
6. At the end you get a full summary and recommendations for what to study next

## Requirements

```
langchain
langchain-core
langchain-groq
langchain-community
langgraph
duckduckgo-search
ddgs
streamlit
python-dotenv
```

## Author

Built by [AbdelazizAushar](https://github.com/AbdelazizAushar)
