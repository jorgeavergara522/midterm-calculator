"""
Memento pattern implementation for undo/redo functionality.
"""

from typing import List, Optional
from copy import deepcopy
from app.calculation import Calculation
from app.exceptions import HistoryError


class CalculatorMemento:
    """
    Memento class that stores a snapshot of calculation history.
    """
    
    def __init__(self, history_snapshot: List[Calculation]):
        """
        Initialize memento with a history snapshot.
        
        Args:
            history_snapshot: Deep copy of calculation history
        """
        self._history_snapshot = deepcopy(history_snapshot)
    
    def get_snapshot(self) -> List[Calculation]:
        """
        Get the stored history snapshot.
        
        Returns:
            Deep copy of the snapshot
        """
        return deepcopy(self._history_snapshot)


class CalculatorCaretaker:
    """
    Caretaker class that manages undo/redo operations using mementos.
    """
    
    def __init__(self):
        """Initialize the caretaker with empty undo/redo stacks."""
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []
    
    def save_state(self, history: List[Calculation]) -> None:
        """
        Save the current state to the undo stack.
        
        Args:
            history: Current calculation history to save
        """
        memento = CalculatorMemento(history)
        self._undo_stack.append(memento)
        
        # Clear redo stack when new state is saved
        self._redo_stack.clear()
    
    def undo(self, current_history: List[Calculation]) -> List[Calculation]:
        """
        Undo the last operation.
        
        Args:
            current_history: Current calculation history
            
        Returns:
            Previous history state
            
        Raises:
            HistoryError: If there's nothing to undo
        """
        if not self._undo_stack:
            raise HistoryError("Nothing to undo")
        
        # Save current state to redo stack
        current_memento = CalculatorMemento(current_history)
        self._redo_stack.append(current_memento)
        
        # Restore previous state
        previous_memento = self._undo_stack.pop()
        return previous_memento.get_snapshot()
    
    def redo(self) -> List[Calculation]:
        """
        Redo the last undone operation.
        
        Returns:
            Next history state
            
        Raises:
            HistoryError: If there's nothing to redo
        """
        if not self._redo_stack:
            raise HistoryError("Nothing to redo")
        
        # Get next state from redo stack
        next_memento = self._redo_stack.pop()
        
        # Save it back to undo stack
        self._undo_stack.append(next_memento)
        
        return next_memento.get_snapshot()
    
    def can_undo(self) -> bool:
        """
        Check if undo is available.
        
        Returns:
            True if undo is possible
        """
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """
        Check if redo is available.
        
        Returns:
            True if redo is possible
        """
        return len(self._redo_stack) > 0
    
    def clear(self) -> None:
        """Clear both undo and redo stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()
    
    def __repr__(self) -> str:
        """Return string representation of caretaker state."""
        return (f"CalculatorCaretaker(undo_stack_size={len(self._undo_stack)}, "
                f"redo_stack_size={len(self._redo_stack)})")
