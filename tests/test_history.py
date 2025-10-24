"""
Unit tests for CalculationHistory.
"""

import pytest
import os
import tempfile
from app.history import CalculationHistory
from app.calculation import Calculation
from app.operations import AddOperation, MultiplyOperation
from app.exceptions import HistoryError


class TestCalculationHistory:
    """Tests for CalculationHistory."""
    
    def test_history_initialization(self):
        """Test history initializes correctly."""
        history = CalculationHistory(max_size=50)
        assert history.get_count() == 0
    
    def test_add_calculation(self):
        """Test adding calculation to history."""
        history = CalculationHistory()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        
        history.add_calculation(calc)
        
        assert history.get_count() == 1
    
    def test_get_history(self):
        """Test getting history returns copy."""
        history = CalculationHistory()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        retrieved = history.get_history()
        
        assert len(retrieved) == 1
        assert retrieved[0] == calc
    
    def test_get_last_calculation(self):
        """Test getting last calculation."""
        history = CalculationHistory()
        calc1 = Calculation(AddOperation(), 5, 3)
        calc2 = Calculation(MultiplyOperation(), 4, 7)
        calc1.execute()
        calc2.execute()
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        last = history.get_last_calculation()
        assert last == calc2
    
    def test_get_last_calculation_empty(self):
        """Test getting last calculation from empty history."""
        history = CalculationHistory()
        assert history.get_last_calculation() is None
    
    def test_clear_history(self):
        """Test clearing history."""
        history = CalculationHistory()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        history.clear_history()
        
        assert history.get_count() == 0
    
    def test_max_size_enforcement(self):
        """Test that history enforces max size."""
        history = CalculationHistory(max_size=2)
        
        calc1 = Calculation(AddOperation(), 1, 1)
        calc2 = Calculation(AddOperation(), 2, 2)
        calc3 = Calculation(AddOperation(), 3, 3)
        
        calc1.execute()
        calc2.execute()
        calc3.execute()
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        history.add_calculation(calc3)
        
        assert history.get_count() == 2
        # First calculation should be removed
        retrieved = history.get_history()
        assert retrieved[0] == calc2
        assert retrieved[1] == calc3
    
    def test_save_to_csv(self):
        """Test saving history to CSV."""
        history = CalculationHistory()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            filepath = f.name
        
        try:
            history.save_to_csv(filepath)
            assert os.path.exists(filepath)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_save_empty_history_raises_error(self):
        """Test saving empty history raises error."""
        history = CalculationHistory()
        
        with pytest.raises(HistoryError, match="No history to save"):
            history.save_to_csv("dummy.csv")
    
    def test_load_from_csv(self):
        """Test loading history from CSV."""
        history = CalculationHistory()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            filepath = f.name
        
        try:
            history.save_to_csv(filepath)
            
            new_history = CalculationHistory()
            new_history.load_from_csv(filepath)
            
            assert new_history.get_count() == 1
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_load_nonexistent_file_raises_error(self):
        """Test loading from nonexistent file raises error."""
        history = CalculationHistory()
        
        with pytest.raises(HistoryError, match="History file not found"):
            history.load_from_csv("nonexistent.csv")
    
    def test_str_representation(self):
        """Test string representation."""
        history = CalculationHistory()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        history.add_calculation(calc)
        
        result = str(history)
        
        assert "Calculation History" in result
        assert "5" in result
    
    def test_str_empty_history(self):
        """Test string representation of empty history."""
        history = CalculationHistory()
        result = str(history)
        assert "No calculations" in result
    
    def test_repr(self):
        """Test detailed representation."""
        history = CalculationHistory(max_size=50)
        result = repr(history)
        assert "CalculationHistory" in result
        assert "50" in result
