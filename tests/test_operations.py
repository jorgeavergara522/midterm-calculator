"""
Unit tests for operation classes.
"""

import pytest
from app.operations import (
    AddOperation, SubtractOperation, MultiplyOperation, DivideOperation,
    PowerOperation, RootOperation, ModulusOperation, IntDivideOperation,
    PercentOperation, AbsDiffOperation, OperationFactory
)
from app.exceptions import OperationError


class TestAddOperation:
    """Tests for AddOperation."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        add = AddOperation()
        assert add.execute(5, 3) == 8
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        add = AddOperation()
        assert add.execute(-5, -3) == -8
    
    def test_add_zero(self):
        """Test adding zero."""
        add = AddOperation()
        assert add.execute(10, 0) == 10
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        add = AddOperation()
        assert add.get_symbol() == "+"


class TestSubtractOperation:
    """Tests for SubtractOperation."""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        subtract = SubtractOperation()
        assert subtract.execute(10, 3) == 7
    
    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative."""
        subtract = SubtractOperation()
        assert subtract.execute(3, 10) == -7
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        subtract = SubtractOperation()
        assert subtract.get_symbol() == "-"


class TestMultiplyOperation:
    """Tests for MultiplyOperation."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        multiply = MultiplyOperation()
        assert multiply.execute(5, 3) == 15
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        multiply = MultiplyOperation()
        assert multiply.execute(10, 0) == 0
    
    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        multiply = MultiplyOperation()
        assert multiply.execute(-5, -3) == 15
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        multiply = MultiplyOperation()
        assert multiply.get_symbol() == "*"


class TestDivideOperation:
    """Tests for DivideOperation."""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        divide = DivideOperation()
        assert divide.execute(10, 2) == 5
    
    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises OperationError."""
        divide = DivideOperation()
        with pytest.raises(OperationError, match="Cannot divide by zero"):
            divide.execute(10, 0)
    
    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        divide = DivideOperation()
        assert divide.execute(-10, 2) == -5
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        divide = DivideOperation()
        assert divide.get_symbol() == "/"


class TestPowerOperation:
    """Tests for PowerOperation."""
    
    def test_power_positive_exponent(self):
        """Test raising to positive power."""
        power = PowerOperation()
        assert power.execute(2, 3) == 8
    
    def test_power_zero_exponent(self):
        """Test raising to power of zero."""
        power = PowerOperation()
        assert power.execute(5, 0) == 1
    
    def test_power_negative_exponent(self):
        """Test raising to negative power."""
        power = PowerOperation()
        assert power.execute(2, -2) == 0.25
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        power = PowerOperation()
        assert power.get_symbol() == "^"


class TestRootOperation:
    """Tests for RootOperation."""
    
    def test_square_root(self):
        """Test calculating square root."""
        root = RootOperation()
        assert root.execute(9, 2) == 3
    
    def test_cube_root(self):
        """Test calculating cube root."""
        root = RootOperation()
        result = root.execute(27, 3)
        assert abs(result - 3) < 0.0001  # Allow small floating point difference
    
    def test_root_zero_divisor_raises_error(self):
        """Test that 0th root raises OperationError."""
        root = RootOperation()
        with pytest.raises(OperationError, match="Cannot calculate 0th root"):
            root.execute(10, 0)
    
    def test_even_root_negative_raises_error(self):
        """Test that even root of negative raises OperationError."""
        root = RootOperation()
        with pytest.raises(OperationError, match="Cannot calculate even root of negative number"):
            root.execute(-9, 2)
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        root = RootOperation()
        assert root.get_symbol() == "√"


class TestModulusOperation:
    """Tests for ModulusOperation."""
    
    def test_modulus_positive_numbers(self):
        """Test modulus with positive numbers."""
        modulus = ModulusOperation()
        assert modulus.execute(10, 3) == 1
    
    def test_modulus_zero_divisor_raises_error(self):
        """Test that modulus with zero raises OperationError."""
        modulus = ModulusOperation()
        with pytest.raises(OperationError, match="Cannot perform modulus with zero divisor"):
            modulus.execute(10, 0)
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        modulus = ModulusOperation()
        assert modulus.get_symbol() == "%"


class TestIntDivideOperation:
    """Tests for IntDivideOperation."""
    
    def test_int_divide_positive_numbers(self):
        """Test integer division with positive numbers."""
        int_divide = IntDivideOperation()
        assert int_divide.execute(10, 3) == 3
    
    def test_int_divide_zero_divisor_raises_error(self):
        """Test that integer division by zero raises OperationError."""
        int_divide = IntDivideOperation()
        with pytest.raises(OperationError, match="Cannot divide by zero"):
            int_divide.execute(10, 0)
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        int_divide = IntDivideOperation()
        assert int_divide.get_symbol() == "//"


class TestPercentOperation:
    """Tests for PercentOperation."""
    
    def test_percent_calculation(self):
        """Test percentage calculation."""
        percent = PercentOperation()
        assert percent.execute(50, 200) == 25.0
    
    def test_percent_zero_denominator_raises_error(self):
        """Test that percentage with zero denominator raises OperationError."""
        percent = PercentOperation()
        with pytest.raises(OperationError, match="Cannot calculate percentage with zero denominator"):
            percent.execute(50, 0)
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        percent = PercentOperation()
        assert percent.get_symbol() == "%of"


class TestAbsDiffOperation:
    """Tests for AbsDiffOperation."""
    
    def test_abs_diff_positive_result(self):
        """Test absolute difference with positive result."""
        abs_diff = AbsDiffOperation()
        assert abs_diff.execute(10, 3) == 7
    
    def test_abs_diff_negative_input(self):
        """Test absolute difference with negative input."""
        abs_diff = AbsDiffOperation()
        assert abs_diff.execute(3, 10) == 7
    
    def test_get_symbol(self):
        """Test get_symbol returns correct symbol."""
        abs_diff = AbsDiffOperation()
        assert abs_diff.get_symbol() == "|diff|"


class TestOperationFactory:
    """Tests for OperationFactory."""
    
    def test_create_add_operation(self):
        """Test factory creates AddOperation."""
        operation = OperationFactory.create_operation('add')
        assert isinstance(operation, AddOperation)
    
    def test_create_operation_case_insensitive(self):
        """Test factory is case insensitive."""
        operation = OperationFactory.create_operation('ADD')
        assert isinstance(operation, AddOperation)
    
    def test_create_unknown_operation_raises_error(self):
        """Test that unknown operation raises OperationError."""
        with pytest.raises(OperationError, match="Unknown operation"):
            OperationFactory.create_operation('invalid')
    
    def test_get_available_operations(self):
        """Test get_available_operations returns all operations."""
        operations = OperationFactory.get_available_operations()
        assert 'add' in operations
        assert 'subtract' in operations
        assert len(operations) == 10
