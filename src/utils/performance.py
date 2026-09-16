"""Performance monitoring utilities"""

import time
import functools
from typing import Any, Callable, TypeVar
from src.core.logger import setup_logger

logger = setup_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class timer:
    """Context manager for timing code blocks"""

    def __init__(self, name: str = "Operation"):
        """Initialize timer

        Args:
            name: Name of the operation being timed
        """
        self.name = name
        self.start = None
        self.end = None

    def __enter__(self):
        """Start timing"""
        self.start = time.time()
        return self

    def __exit__(self, *args):
        """End timing and log result"""
        self.end = time.time()
        elapsed = self.end - self.start
        logger.info(f"{self.name} took {elapsed:.3f}s")

    @property
    def elapsed(self) -> float:
        """Get elapsed time"""
        if self.start and self.end:
            return self.end - self.start
        return 0.0


def profile_function(func: F) -> F:
    """Decorator to profile function execution time

    Args:
        func: Function to profile

    Returns:
        Wrapped function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with timer(f"Function {func.__name__}"):
            return func(*args, **kwargs)

    return wrapper
