"""
Unit tests for input validators.
"""

import pytest
from app.input_validators import (
    validate_number, validate_in_range, validate_not_zero, validate_positive
)
from app.exceptions import ValidationError


def test_validate_number_with_int():
    """Test validating an integer."""
    result = validate_number(5)
    assert result == 5.0


def test_validate_number_with_float():
    """Test validating a float."""
    result = validate_number(5.5)
    assert result == 5.5


def test_validate_number_with_string_number():
    """Test validating a string number."""
    result = validate_number("10")
    assert result == 10.0


def test_validate_number_with_invalid_string():
    """Test that invalid string raises error."""
    with pytest.raises(ValidationError, match="must be a number"):
        validate_number("hello")


def test_validate_in_range_within_limit():
    """Test number within range."""
    validate_in_range(100, 1000)  # Should not raise


def test_validate_in_range_exceeds_limit():
    """Test number exceeding range raises error."""
    with pytest.raises(ValidationError, match="exceeds maximum"):
        validate_in_range(5000, 1000)


def test_validate_not_zero_with_nonzero():
    """Test non-zero value."""
    validate_not_zero(5)  # Should not raise


def test_validate_not_zero_with_zero():
    """Test zero raises error."""
    with pytest.raises(ValidationError, match="cannot be zero"):
        validate_not_zero(0)


def test_validate_positive_with_positive():
    """Test positive number."""
    validate_positive(10)  # Should not raise


def test_validate_positive_with_negative():
    """Test negative raises error."""
    with pytest.raises(ValidationError, match="must be positive"):
        validate_positive(-5)


def test_validate_positive_with_zero():
    """Test zero raises error."""
    with pytest.raises(ValidationError, match="must be positive"):
        validate_positive(0)
