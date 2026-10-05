from agents.core import Agent
from agents.skills import build_default_skills

def test_default_skills_are_registered_and_callable():
    agent = Agent()
    for name, handler in build_default_skills().items():
        agent.register_skill(name, handler)
    assert agent.list_skills() == ["code", "research", "verify"]
    result = agent.run("find AI announcements", "research")
    assert result.status == "completed"
    assert result.attempts == 1

def test_unknown_skill_fails_cleanly():
    result = Agent().run("hello", "missing")
    assert result.status == "failed"
    assert "Unknown skill" in (result.error or "")
