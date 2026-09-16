"""Tests for utility modules"""

import pytest
from src.utils.validators import validate_api_key, validate_json
from src.core.exceptions import ConfigurationError


def test_validate_api_key_valid():
    """Test valid API key validation"""
    validate_api_key("sk-1234567890abcdefghij")  # Should not raise


def test_validate_api_key_missing():
    """Test missing API key validation"""
    with pytest.raises(ConfigurationError):
        validate_api_key(None)


def test_validate_api_key_invalid():
    """Test invalid API key validation"""
    with pytest.raises(ConfigurationError):
        validate_api_key("short")


def test_validate_json_valid():
    """Test valid JSON validation"""
    result = validate_json('{"key": "value"}')
    assert result == {"key": "value"}


def test_validate_json_invalid():
    """Test invalid JSON validation"""
    with pytest.raises(ValueError):
        validate_json("{invalid json}")
