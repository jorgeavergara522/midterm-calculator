"""
Custom exception classes for the calculator application.
"""


class CalculatorError(Exception):
    """Base exception class for calculator errors."""
    pass


class OperationError(CalculatorError):
    """Raised when an operation fails or is invalid."""
    pass


class ValidationError(CalculatorError):
    """Raised when input validation fails."""
    pass


class HistoryError(CalculatorError):
    """Raised when history operations fail."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when configuration loading fails."""
    pass
