"""Built-in safe skills for the self-hosted agent."""

from typing import Callable

def research_skill(task: str) -> str:
    return f"Research task queued: {task}"

def verify_skill(task: str) -> str:
    return f"Verification task queued: {task}"

def code_skill(task: str) -> str:
    return f"Code task queued: {task}"

def build_default_skills() -> dict[str, Callable[[str], str]]:
    return {"research": research_skill, "verify": verify_skill, "code": code_skill}
