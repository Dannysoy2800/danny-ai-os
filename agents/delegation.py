"""Free-first task delegation with bounded retries and quality checks.

No network clients or paid providers are enabled by default. Integrations must be
explicitly registered by the application.
"""
from dataclasses import dataclass, field
from typing import Callable, Protocol


class ToolAdapter(Protocol):
    name: str
    priority: int
    cost_tier: str  # "local" or "free"; paid adapters are deliberately excluded.

    def run(self, task: str) -> str: ...


@dataclass
class DelegationResult:
    status: str
    output: str | None
    tool: str | None = None
    attempts: int = 0
    error: str | None = None
    quality_checked: bool = False
    errors: list[str] = field(default_factory=list)


class FreeFirstDelegator:
    """Route to local/free adapters only; never silently fall back to paid tools."""

    def __init__(
        self,
        tools: list[ToolAdapter] | None = None,
        reviewer: Callable[[str, str], bool] | None = None,
        max_retries: int = 2,
    ) -> None:
        self.tools = sorted(
            [tool for tool in (tools or []) if tool.cost_tier in {"local", "free"}],
            key=lambda tool: (0 if tool.cost_tier == "local" else 1, tool.priority),
        )
        self.reviewer = reviewer
        self.max_retries = max(1, min(max_retries, 3))

    def delegate(self, task: str) -> DelegationResult:
        if not task.strip():
            return DelegationResult("failed", None, error="Task is empty")
        if not self.tools:
            return DelegationResult(
                "blocked", None,
                error="No local/free tool is configured; no paid fallback was attempted.",
            )

        errors: list[str] = []
        attempts = 0
        for tool in self.tools:
            for _ in range(self.max_retries):
                attempts += 1
                try:
                    output = tool.run(task)
                    if not isinstance(output, str) or not output.strip():
                        raise ValueError("Tool returned empty or non-text output")
                    if self.reviewer is not None:
                        if not self.reviewer(task, output):
                            errors.append(f"{tool.name}: quality review rejected output")
                            continue
                        return DelegationResult(
                            "completed", output, tool.name, attempts,
                            quality_checked=True, errors=errors.copy(),
                        )
                    return DelegationResult(
                        "completed", output, tool.name, attempts,
                        quality_checked=False, errors=errors.copy(),
                    )
                except Exception as exc:
                    # Avoid exposing arbitrary exception text in user-facing output.
                    errors.append(f"{tool.name}: {type(exc).__name__}")
        return DelegationResult(
            "failed", None, attempts=attempts,
            error="All configured local/free tools failed or failed quality review.",
            errors=errors,
        )
