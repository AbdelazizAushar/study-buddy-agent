from ddgs import DDGS
from langchain.tools import tool

ddgs = DDGS()


@tool
def web_search(query: str) -> str:
    """Searches the web and returns the results."""
    return ddgs.text(query, max_results=5)


progress = {"current_lesson": 0, "score": 0, "total": 0}


@tool
def track_progress(correct: bool) -> str:
    """Updates the user's score and lesson progress."""
    progress["total"] += 1
    if correct:
        progress["score"] += 1
    progress["current_lesson"] += 1
    return f"Lesson {progress['current_lesson']} | Score: {progress['score']}/{progress['total']}"


@tool
def reset_progress() -> str:
    """Resets the user's progress for a new session."""
    progress["current_lesson"] = 0
    progress["score"] = 0
    progress["total"] = 0
    return "Progress reset. Ready for a new session!"
