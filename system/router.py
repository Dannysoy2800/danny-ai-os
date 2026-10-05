"""Local/free-first provider router with bounded retry and failover."""

from dataclasses import dataclass
from typing import Iterable
from .provider import Provider, ProviderStatus

@dataclass
class RoutingResult:
    provider: str | None
    output: str | None
    attempts: int
    errors: list[str]

class ProviderRouter:
    def __init__(self, providers: Iterable[Provider], max_retries: int = 3) -> None:
        self.providers = sorted(providers, key=lambda p: p.priority)
        self.max_retries = max(1, max_retries)

    def health(self) -> list[ProviderStatus]:
        return [ProviderStatus(p.name, bool(getattr(p, "healthy", True))) for p in self.providers]

    def generate(self, prompt: str) -> RoutingResult:
        errors: list[str] = []
        attempts = 0
        for provider in self.providers:
            if not getattr(provider, "healthy", True):
                continue
            for _ in range(self.max_retries):
                attempts += 1
                try:
                    return RoutingResult(provider.name, provider.generate(prompt), attempts, errors)
                except Exception as exc:
                    errors.append(f"{provider.name}: {exc}")
        return RoutingResult(None, None, attempts, errors)
