import streamlit as st
import uuid

# Import agent components and state tools based on project context
from agent.agent import agent
from agent.tools import progress, reset_progress

# --- Session State Initialization ---
if "session_started" not in st.session_state:
    st.session_state.session_started = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "config" not in st.session_state:
    st.session_state.config = {
        "configurable": {"thread_id": st.session_state.thread_id}
    }

# --- Sidebar: Progress Tracking & Controls ---
with st.sidebar:
    st.header("📊 Study Progress")

    # Display live progress dict values (updates automatically on st.rerun)
    st.metric("Current Lesson", progress.get("current_lesson", 0))
    st.metric("Score", progress.get("score", 0))
    st.metric("Total", progress.get("total", 0))

    st.divider()

    # Reset tool and session handler
    if st.button("New Session", use_container_width=True):
        reset_progress.invoke({})
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.config["configurable"]["thread_id"] = st.session_state.thread_id
        st.session_state.messages = []
        st.session_state.session_started = False
        st.rerun()

# --- Main Application Interface ---
st.title("🧠 Study Buddy AI")

# 1. Setup Interface (First Load)
if not st.session_state.session_started:
    st.write("Welcome! Let's set up your study session.")

    topic = st.text_input("What topic are you studying?",
                          placeholder="e.g., Neural Networks, NLP, Computer Vision")
    goal = st.text_input("What is your learning goal?",
                         placeholder="e.g., Master transformers for NLP tasks")

    if st.button("Start Session", type="primary"):
        if topic and goal:
            st.session_state.session_started = True

            # Formulate the initial context message
            initial_prompt = f"I want to study {topic}. My learning goal is: {goal}."
            st.session_state.messages.append(
                {"role": "user", "content": initial_prompt})

            # Link thread ID to config for memory persistence
            st.session_state.config["configurable"]["thread_id"] = st.session_state.thread_id

            with st.spinner("Preparing your session..."):
                # Initial invoke to start the LangGraph/Agent thread
                response = agent.invoke(
                    {"messages": [("user", initial_prompt)]}, st.session_state.config)

                # Extract only the last AIMessage content
                ai_response = response["messages"][-1].content
                st.session_state.messages.append(
                    {"role": "assistant", "content": ai_response})

            st.rerun()
        else:
            st.warning(
                "Please enter both a topic and a learning goal to begin.")

# 2. Chat Interface (Active Session)
else:
    # Render message history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle new user input
    if prompt := st.chat_input("Ask a question or request a quiz..."):

        # Display and save user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Ensure thread config is passed
        st.session_state.config["configurable"]["thread_id"] = st.session_state.thread_id

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Invoke agent with the latest user message
                response = agent.invoke(
                    {"messages": [("user", prompt)]}, st.session_state.config)

                # Display only the last AIMessage content
                ai_response = response["messages"][-1].content
                st.markdown(ai_response)

        # Save assistant response to state
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response})

        # Rerun to ensure the sidebar progress metrics pull the freshest dictionary state
        st.rerun()
