"""
Unit tests for Calculation class.
"""

import pytest
from datetime import datetime
from app.calculation import Calculation
from app.operations import AddOperation, MultiplyOperation, DivideOperation
from app.exceptions import OperationError


class TestCalculation:
    """Tests for Calculation class."""
    
    def test_calculation_initialization(self):
        """Test that calculation initializes correctly."""
        operation = AddOperation()
        calc = Calculation(operation, 5, 3)
        
        assert calc.operation == operation
        assert calc.operand_a == 5
        assert calc.operand_b == 3
        assert calc.result is None
        assert isinstance(calc.timestamp, datetime)
    
    def test_calculation_execute(self):
        """Test that calculation executes correctly."""
        operation = AddOperation()
        calc = Calculation(operation, 5, 3)
        
        result = calc.execute()
        
        assert result == 8
        assert calc.result == 8
    
    def test_calculation_execute_multiply(self):
        """Test calculation with multiplication."""
        operation = MultiplyOperation()
        calc = Calculation(operation, 4, 7)
        
        result = calc.execute()
        
        assert result == 28
        assert calc.result == 28
    
    def test_calculation_execute_with_error(self):
        """Test that calculation propagates operation errors."""
        operation = DivideOperation()
        calc = Calculation(operation, 10, 0)
        
        with pytest.raises(OperationError):
            calc.execute()
    
    def test_calculation_str_with_result(self):
        """Test string representation with result."""
        operation = AddOperation()
        calc = Calculation(operation, 5, 3)
        calc.execute()
        
        result_str = str(calc)
        
        assert "5" in result_str
        assert "3" in result_str
        assert "8" in result_str
        assert "+" in result_str
    
    def test_calculation_str_without_result(self):
        """Test string representation without result."""
        operation = AddOperation()
        calc = Calculation(operation, 5, 3)
        
        result_str = str(calc)
        
        assert "5" in result_str
        assert "3" in result_str
        assert "+" in result_str
    
    def test_calculation_repr(self):
        """Test detailed representation."""
        operation = AddOperation()
        calc = Calculation(operation, 5, 3)
        calc.execute()
        
        repr_str = repr(calc)
        
        assert "Calculation" in repr_str
        assert "AddOperation" in repr_str
        assert "5" in repr_str
        assert "3" in repr_str
    
    def test_calculation_to_dict(self):
        """Test conversion to dictionary."""
        operation = AddOperation()
        calc = Calculation(operation, 5, 3)
        calc.execute()
        
        calc_dict = calc.to_dict()
        
        assert calc_dict['operation'] == 'add'
        assert calc_dict['operand_a'] == 5
        assert calc_dict['operand_b'] == 3
        assert calc_dict['result'] == 8
        assert 'timestamp' in calc_dict
    
    def test_calculation_to_dict_before_execute(self):
        """Test to_dict before execution."""
        operation = MultiplyOperation()
        calc = Calculation(operation, 4, 5)
        
        calc_dict = calc.to_dict()
        
        assert calc_dict['operation'] == 'multiply'
        assert calc_dict['operand_a'] == 4
        assert calc_dict['operand_b'] == 5
        assert calc_dict['result'] is None
        assert 'timestamp' in calc_dict
