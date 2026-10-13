"""Built-in skills that delegate work to explicitly configured adapters."""
from typing import Callable

from agents.delegation import DelegationResult, FreeFirstDelegator


def _skill(delegator: FreeFirstDelegator, task: str) -> DelegationResult:
    return delegator.delegate(task)


def build_default_skills(
    delegator: FreeFirstDelegator | None = None,
) -> dict[str, Callable[[str], DelegationResult]]:
    """Build skills around an injected free-first delegator.

    With no integrations configured, skills return BLOCKED rather than pretending
    a task was queued or completed.
    """
    router = delegator or FreeFirstDelegator()
    return {
        "research": lambda task: _skill(router, task),
        "verify": lambda task: _skill(router, task),
        "code": lambda task: _skill(router, task),
    }
