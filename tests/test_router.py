from system.router import ProviderRouter

class FailingProvider:
    name = "local"
    priority = 0
    healthy = True
    def generate(self, prompt: str) -> str:
        raise RuntimeError("offline")

class WorkingProvider:
    name = "free-api"
    priority = 1
    healthy = True
    def generate(self, prompt: str) -> str:
        return f"ok: {prompt}"

def test_router_fails_over_after_retries():
    result = ProviderRouter([FailingProvider(), WorkingProvider()], max_retries=2).generate("hello")
    assert result.provider == "free-api"
    assert result.output == "ok: hello"
    assert result.attempts == 3
    assert len(result.errors) == 2
