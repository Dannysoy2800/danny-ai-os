"""Minimal self-hosted agent runtime with pluggable skills."""

from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass
class AgentResult:
    status: str
    output: Any
    skill: str | None = None
    attempts: int = 0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

class Agent:
    def __init__(self) -> None:
        self._skills: dict[str, Callable[[str], Any]] = {}

    def register_skill(self, name: str, handler: Callable[[str], Any]) -> None:
        if not name.strip():
            raise ValueError("Skill name cannot be empty")
        self._skills[name] = handler

    def list_skills(self) -> list[str]:
        return sorted(self._skills)

    def run(self, task: str, skill: str) -> AgentResult:
        if not task.strip():
            return AgentResult("failed", None, skill=skill, error="Task is empty")
        handler = self._skills.get(skill)
        if handler is None:
            return AgentResult("failed", None, skill=skill, error=f"Unknown skill: {skill}")
        try:
            return AgentResult("completed", handler(task), skill=skill, attempts=1)
        except Exception as exc:
            return AgentResult("failed", None, skill=skill, attempts=1, error=str(exc))
