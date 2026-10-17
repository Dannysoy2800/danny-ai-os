from agents.delegation import FreeFirstDelegator


class FakeTool:
    def __init__(self, name, priority, cost_tier, output=None, error=None):
        self.name = name
        self.priority = priority
        self.cost_tier = cost_tier
        self.output = output
        self.error = error
        self.calls = 0

    def run(self, task):
        self.calls += 1
        if self.error:
            raise RuntimeError(self.error)
        return self.output


def test_local_tool_is_preferred_and_quality_checked():
    free = FakeTool("free", 0, "free", "reviewed answer")
    local = FakeTool("local", 99, "local", "local answer")
    result = FreeFirstDelegator(
        [free, local], reviewer=lambda task, output: output == "local answer"
    ).delegate("research this")
    assert result.status == "completed"
    assert result.tool == "local"
    assert result.quality_checked is True
    assert free.calls == 0


def test_failed_local_falls_back_to_free_tool_with_bounded_retries():
    local = FakeTool("local", 0, "local", error="offline token=secret")
    free = FakeTool("free", 0, "free", "answer")
    result = FreeFirstDelegator([free, local], max_retries=2).delegate("task")
    assert result.status == "completed"
    assert result.tool == "free"
    assert result.attempts == 3
    assert local.calls == 2
    assert free.calls == 1
    assert result.errors == ["local: RuntimeError", "local: RuntimeError"]
    assert all("secret" not in error for error in result.errors)


def test_paid_tool_is_never_selected():
    paid = FakeTool("paid", 0, "paid", "paid answer")
    result = FreeFirstDelegator([paid]).delegate("task")
    assert result.status == "blocked"
    assert paid.calls == 0


def test_quality_rejection_retries_same_adapter_before_failing_over():
    tool = FakeTool("free", 0, "free", "answer")
    review_calls = 0

    def reviewer(task, output):
        nonlocal review_calls
        review_calls += 1
        return review_calls == 2

    result = FreeFirstDelegator([tool], reviewer=reviewer, max_retries=2).delegate("task")
    assert result.status == "completed"
    assert result.quality_checked is True
    assert result.attempts == 2
    assert tool.calls == 2
    assert result.errors == ["free: quality review rejected output"]


def test_quality_rejection_does_not_report_success_after_retry_budget():
    tool = FakeTool("free", 0, "free", "unverified answer")
    result = FreeFirstDelegator([tool], reviewer=lambda task, output: False, max_retries=2).delegate("task")
    assert result.status == "failed"
    assert result.output is None
    assert tool.calls == 2
    assert len(result.errors) == 2


def test_empty_output_is_rejected():
    tool = FakeTool("free", 0, "free", "  ")
    result = FreeFirstDelegator([tool], max_retries=1).delegate("task")
    assert result.status == "failed"
    assert result.output is None
    assert result.errors == ["free: ValueError"]
