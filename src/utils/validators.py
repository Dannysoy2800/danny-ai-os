"""Input validation utilities"""

import json
from typing import Any, Dict
from src.core.exceptions import ConfigurationError


def validate_api_key(api_key: str | None, key_name: str = "API_KEY") -> None:
    """Validate API key format

    Args:
        api_key: API key to validate
        key_name: Name of the API key for error messages

    Raises:
        ConfigurationError: If API key is invalid
    """
    if not api_key:
        raise ConfigurationError(f"{key_name} is not configured")
    if len(api_key) < 10:
        raise ConfigurationError(f"{key_name} appears to be invalid (too short)")


def validate_json(data: str) -> Dict[str, Any]:
    """Validate and parse JSON string

    Args:
        data: JSON string to validate

    Returns:
        Parsed JSON data

    Raises:
        ValueError: If JSON is invalid
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")
