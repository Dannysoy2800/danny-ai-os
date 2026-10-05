"""Provider abstraction for the routing layer."""

from dataclasses import dataclass
from typing import Protocol

class Provider(Protocol):
    name: str
    priority: int
    def generate(self, prompt: str) -> str: ...

@dataclass(frozen=True)
class ProviderStatus:
    name: str
    healthy: bool
    reason: str = ""
