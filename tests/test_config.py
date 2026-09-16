"""Tests for configuration module"""

import pytest
from src.core.config import Settings


def test_default_settings():
    """Test default settings values"""
    settings = Settings()
    assert settings.app_name == "Danny AI OS"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "development"


def test_custom_settings():
    """Test custom settings values"""
    settings = Settings(
        app_name="Custom AI",
        environment="production",
        debug=True,
    )
    assert settings.app_name == "Custom AI"
    assert settings.environment == "production"
    assert settings.debug is True
