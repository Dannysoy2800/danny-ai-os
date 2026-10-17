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
        # Fail closed: providers without an explicit local/free tier are excluded.
        eligible = [p for p in providers if getattr(p, "cost_tier", None) in {"local", "free"}]
        self.providers = sorted(
            eligible,
            key=lambda p: (0 if p.cost_tier == "local" else 1, p.priority),
        )
        self.max_retries = max(1, min(max_retries, 3))

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
                    # Never expose arbitrary provider exception text (it may contain secrets).
                    errors.append(f"{provider.name}: {type(exc).__name__}")
        return RoutingResult(None, None, attempts, errors)
