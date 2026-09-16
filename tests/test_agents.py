"""Tests for agent modules"""

import pytest
from src.agents.manager import ManagerAgent


def test_manager_agent_initialization():
    """Test ManagerAgent initialization"""
    agent = ManagerAgent()
    assert agent is not None
    assert agent.graph is not None


def test_manager_agent_execution():
    """Test ManagerAgent execution"""
    agent = ManagerAgent()
    result = agent.execute("Test message")
    assert result is not None
    assert result["status"] == "completed"
    assert result["error"] is None
