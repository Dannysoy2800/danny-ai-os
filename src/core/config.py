"""Configuration management for Danny AI OS

Uses pydantic-settings for environment variable handling.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = Field(default="Danny AI OS", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")
    environment: str = Field(default="development", description="Environment (development, production, testing)")

    # API Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4", description="Default OpenAI model")

    # LangGraph Configuration
    langgraph_debug: bool = Field(default=False, description="Enable LangGraph debug mode")
    langgraph_timeout: int = Field(default=30, description="LangGraph timeout in seconds")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json or text)")
    log_file: Optional[str] = Field(default=None, description="Log file path")

    # Performance
    enable_profiling: bool = Field(default=False, description="Enable performance profiling")
    max_concurrent_tasks: int = Field(default=10, description="Maximum concurrent tasks")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
