"""Provider abstraction for the routing layer."""

from dataclasses import dataclass
from typing import Protocol


class Provider(Protocol):
    name: str
    priority: int
    cost_tier: str  # Must be explicitly "local" or "free" to be eligible.

    def generate(self, prompt: str) -> str: ...


@dataclass(frozen=True)
class ProviderStatus:
    name: str
    healthy: bool
    reason: str = ""
