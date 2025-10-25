"""
Unit tests for Calculator Memento pattern.
"""

import pytest
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.calculation import Calculation
from app.operations import AddOperation
from app.exceptions import HistoryError


class TestCalculatorMemento:
    """Tests for CalculatorMemento."""
    
    def test_memento_stores_snapshot(self):
        """Test memento stores history snapshot."""
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        history = [calc]
        
        memento = CalculatorMemento(history)
        snapshot = memento.get_snapshot()
        
        assert len(snapshot) == 1
        assert snapshot[0].result == 8


class TestCalculatorCaretaker:
    """Tests for CalculatorCaretaker."""
    
    def test_caretaker_initialization(self):
        """Test caretaker initializes with empty stacks."""
        caretaker = CalculatorCaretaker()
        
        assert not caretaker.can_undo()
        assert not caretaker.can_redo()
    
    def test_save_state(self):
        """Test saving state to undo stack."""
        caretaker = CalculatorCaretaker()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        history = [calc]
        
        caretaker.save_state(history)
        
        assert caretaker.can_undo()
    
    def test_undo(self):
        """Test undo operation."""
        caretaker = CalculatorCaretaker()
        calc1 = Calculation(AddOperation(), 5, 3)
        calc2 = Calculation(AddOperation(), 10, 5)
        calc1.execute()
        calc2.execute()
        
        history1 = [calc1]
        history2 = [calc1, calc2]
        
        caretaker.save_state(history1)
        
        restored = caretaker.undo(history2)
        
        assert len(restored) == 1
        assert caretaker.can_redo()
    
    def test_undo_empty_raises_error(self):
        """Test undo with empty stack raises error."""
        caretaker = CalculatorCaretaker()
        
        with pytest.raises(HistoryError, match="Nothing to undo"):
            caretaker.undo([])
    
    def test_redo(self):
        """Test redo operation."""
        caretaker = CalculatorCaretaker()
        calc1 = Calculation(AddOperation(), 5, 3)
        calc2 = Calculation(AddOperation(), 10, 5)
        calc1.execute()
        calc2.execute()
        
        history1 = [calc1]
        history2 = [calc1, calc2]
        
        caretaker.save_state(history1)
        caretaker.undo(history2)
        
        restored = caretaker.redo()
        
        assert len(restored) == 2
    
    def test_redo_empty_raises_error(self):
        """Test redo with empty stack raises error."""
        caretaker = CalculatorCaretaker()
        
        with pytest.raises(HistoryError, match="Nothing to redo"):
            caretaker.redo()
    
    def test_save_clears_redo_stack(self):
        """Test that saving new state clears redo stack."""
        caretaker = CalculatorCaretaker()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        
        caretaker.save_state([calc])
        caretaker.undo([calc])
        
        assert caretaker.can_redo()
        
        caretaker.save_state([calc])
        
        assert not caretaker.can_redo()
    
    def test_clear(self):
        """Test clearing both stacks."""
        caretaker = CalculatorCaretaker()
        calc = Calculation(AddOperation(), 5, 3)
        calc.execute()
        
        caretaker.save_state([calc])
        caretaker.clear()
        
        assert not caretaker.can_undo()
        assert not caretaker.can_redo()
    
    def test_repr(self):
        """Test string representation."""
        caretaker = CalculatorCaretaker()
        repr_str = repr(caretaker)
        
        assert "CalculatorCaretaker" in repr_str
