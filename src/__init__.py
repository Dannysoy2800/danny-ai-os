"""Danny AI OS - Personal AI Operating System

A comprehensive Python-based intelligent automation platform with LangGraph integration.
"""

__version__ = "0.1.0"
__author__ = "Danny"
__license__ = "MIT"

from src.core.config import settings
from src.core.logger import setup_logger

__all__ = ["settings", "setup_logger"]
