from system.router import ProviderRouter


class FailingProvider:
    name = "local"
    priority = 0
    cost_tier = "local"
    healthy = True

    def generate(self, prompt: str) -> str:
        raise RuntimeError("offline token=secret-value")


class WorkingProvider:
    name = "free-api"
    priority = 1
    cost_tier = "free"
    healthy = True

    def generate(self, prompt: str) -> str:
        return f"ok: {prompt}"


class PaidProvider:
    name = "paid-api"
    priority = -100
    cost_tier = "paid"
    healthy = True
    calls = 0

    def generate(self, prompt: str) -> str:
        self.calls += 1
        return "paid response"


def test_router_fails_over_after_retries_and_redacts_errors():
    result = ProviderRouter([FailingProvider(), WorkingProvider()], max_retries=2).generate("hello")
    assert result.provider == "free-api"
    assert result.output == "ok: hello"
    assert result.attempts == 3
    assert result.errors == ["local: RuntimeError", "local: RuntimeError"]
    assert all("secret-value" not in error for error in result.errors)


def test_router_excludes_paid_providers_even_with_higher_priority():
    paid = PaidProvider()
    result = ProviderRouter([paid, WorkingProvider()]).generate("hello")
    assert result.provider == "free-api"
    assert paid.calls == 0


def test_router_caps_retries_at_three():
    result = ProviderRouter([FailingProvider()], max_retries=100).generate("hello")
    assert result.attempts == 3
    assert len(result.errors) == 3
