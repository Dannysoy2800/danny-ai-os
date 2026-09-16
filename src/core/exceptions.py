"""Custom exceptions for Danny AI OS"""


class DannyAIOSError(Exception):
    """Base exception for Danny AI OS"""

    pass


class ConfigurationError(DannyAIOSError):
    """Raised when configuration is invalid"""

    pass


class AgentError(DannyAIOSError):
    """Raised when agent operation fails"""

    pass


class WorkflowError(DannyAIOSError):
    """Raised when workflow execution fails"""

    pass


class APIError(DannyAIOSError):
    """Raised when API call fails"""

    pass


class TimeoutError(DannyAIOSError):
    """Raised when operation times out"""

    pass
