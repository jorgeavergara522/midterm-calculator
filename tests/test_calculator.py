"""
Unit tests for Calculator class.
"""

import pytest
import os
import tempfile
from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.exceptions import OperationError, ValidationError, HistoryError


class TestCalculator:
    """Tests for Calculator class."""
    
    def test_calculator_initialization(self):
        """Test calculator initializes correctly."""
        calc = Calculator()
        
        assert calc.config is not None
        assert calc.logger is not None
        assert calc.history is not None
        assert calc.caretaker is not None
        assert len(calc.observers) >= 1  # At least logging observer
    
    def test_perform_calculation_add(self):
        """Test performing addition."""
        calc = Calculator()
        
        result = calc.perform_calculation('add', 5, 3)
        
        assert result == 8.0
        assert calc.history.get_count() == 1
    
    def test_perform_calculation_multiply(self):
        """Test performing multiplication."""
        calc = Calculator()
        
        result = calc.perform_calculation('multiply', 4, 7)
        
        assert result == 28.0
    
    def test_perform_calculation_with_validation_error(self):
        """Test calculation with invalid input."""
        calc = Calculator()
        
        with pytest.raises(ValidationError):
            calc.perform_calculation('add', 'hello', 3)
    
    def test_perform_calculation_with_operation_error(self):
        """Test calculation with operation error."""
        calc = Calculator()
        
        with pytest.raises(OperationError):
            calc.perform_calculation('divide', 10, 0)
    
    def test_undo(self):
        """Test undo functionality."""
        calc = Calculator()
        calc.perform_calculation('add', 5, 3)
        calc.perform_calculation('add', 10, 5)
        
        calc.undo()
        
        assert calc.history.get_count() == 1
    
    def test_undo_empty_raises_error(self):
        """Test undo with no history raises error."""
        calc = Calculator()
        
        with pytest.raises(HistoryError):
            calc.undo()
    
    def test_redo(self):
        """Test redo functionality."""
        calc = Calculator()
        calc.perform_calculation('add', 5, 3)
        calc.undo()
        
        calc.redo()
        
        assert calc.history.get_count() == 1
    
    def test_redo_empty_raises_error(self):
        """Test redo with nothing to redo raises error."""
        calc = Calculator()
        
        with pytest.raises(HistoryError):
            calc.redo()
    
    def test_clear_history(self):
        """Test clearing history."""
        calc = Calculator()
        calc.perform_calculation('add', 5, 3)
        
        calc.clear_history()
        
        assert calc.history.get_count() == 0
    
    def test_save_history(self):
        """Test saving history to file."""
        calc = Calculator()
        calc.perform_calculation('add', 5, 3)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            filepath = f.name
        
        calc.config.history_file = filepath
        
        try:
            calc.save_history()
            assert os.path.exists(filepath)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_load_history(self):
        """Test loading history from file."""
        calc = Calculator()
        calc.perform_calculation('add', 5, 3)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            filepath = f.name
        
        calc.config.history_file = filepath
        
        try:
            calc.save_history()
            
            new_calc = Calculator()
            new_calc.config.history_file = filepath
            new_calc.load_history()
            
            assert new_calc.history.get_count() >= 1
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_register_observer(self):
        """Test registering an observer."""
        calc = Calculator()
        initial_count = len(calc.observers)
        
        from app.calculation import Calculation
        from app.operations import AddOperation
        
        class DummyObserver:
            def update(self, calculation):
                pass
        
        calc.register_observer(DummyObserver())
        
        assert len(calc.observers) == initial_count + 1


class TestLoggingObserver:
    """Tests for LoggingObserver."""
    
    def test_logging_observer_update(self):
        """Test logging observer logs calculation."""
        from app.logger import Logger
        from app.calculation import Calculation
        from app.operations import AddOperation
        
        logger = Logger()
        observer = LoggingObserver(logger)
        
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        
        # Should not raise error
        observer.update(calc)


class TestAutoSaveObserver:
    """Tests for AutoSaveObserver."""
    
    def test_autosave_observer_update(self):
        """Test auto-save observer saves on update."""
        from app.history import CalculationHistory
        from app.calculation import Calculation
        from app.operations import AddOperation
        
        history = CalculationHistory()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            filepath = f.name
        
        try:
            observer = AutoSaveObserver(history, filepath)
            observer.update(calc)
            
            assert os.path.exists(filepath)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
