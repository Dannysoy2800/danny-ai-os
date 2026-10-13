from agents.core import Agent
from agents.skills import build_default_skills
from agents.delegation import FreeFirstDelegator


def test_default_skills_are_registered_and_block_without_integrations():
    agent = Agent()
    for name, handler in build_default_skills().items():
        agent.register_skill(name, handler)
    assert agent.list_skills() == ["code", "research", "verify"]
    result = agent.run("find AI announcements", "research")
    assert result.status == "blocked"
    assert "no paid fallback" in (result.error or "")
    assert result.metadata["quality_checked"] is False


def test_unknown_skill_fails_cleanly():
    result = Agent().run("hello", "missing")
    assert result.status == "failed"
    assert "Unknown skill" in (result.error or "")


def test_empty_task_fails_cleanly():
    result = Agent().run("   ", "research")
    assert result.status == "failed"
    assert result.error == "Task is empty"
