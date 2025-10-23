"""
Input validation functions for the calculator.
"""

from app.exceptions import ValidationError


def validate_number(value, param_name: str = "value") -> float:
    """
    Validate that a value is a number.
    
    Args:
        value: The value to validate
        param_name: Name of the parameter for error messages
        
    Returns:
        The value as a float
        
    Raises:
        ValidationError: If value is not a number
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"{param_name} must be a number, got '{value}'")


def validate_in_range(value: float, max_value: float, param_name: str = "value") -> None:
    """
    Validate that a number is within the allowed range.
    
    Args:
        value: The value to validate
        max_value: Maximum allowed value
        param_name: Name of the parameter for error messages
        
    Raises:
        ValidationError: If value exceeds max_value
    """
    if abs(value) > max_value:
        raise ValidationError(f"{param_name} exceeds maximum allowed value of {max_value}")


def validate_not_zero(value: float, param_name: str = "value") -> None:
    """
    Validate that a number is not zero.
    
    Args:
        value: The value to validate
        param_name: Name of the parameter for error messages
        
    Raises:
        ValidationError: If value is zero
    """
    if value == 0:
        raise ValidationError(f"{param_name} cannot be zero")


def validate_positive(value: float, param_name: str = "value") -> None:
    """
    Validate that a number is positive.
    
    Args:
        value: The value to validate
        param_name: Name of the parameter for error messages
        
    Raises:
        ValidationError: If value is not positive
    """
    if value <= 0:
        raise ValidationError(f"{param_name} must be positive, got {value}")
