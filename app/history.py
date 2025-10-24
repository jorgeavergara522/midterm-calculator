"""
History management for calculator calculations.
Handles storing, saving, and loading calculation history using pandas.
"""

import pandas as pd
from datetime import datetime
from typing import List, Optional
from app.calculation import Calculation
from app.operations import OperationFactory
from app.exceptions import HistoryError


class CalculationHistory:
    """Manages the history of calculations."""
    
    def __init__(self, max_size: int = 100):
        """
        Initialize calculation history.
        
        Args:
            max_size: Maximum number of calculations to store
        """
        self._history: List[Calculation] = []
        self._max_size = max_size
    
    def add_calculation(self, calculation: Calculation) -> None:
        """
        Add a calculation to history.
        
        Args:
            calculation: The calculation to add
        """
        self._history.append(calculation)
        
        # Remove oldest if exceeding max size
        if len(self._history) > self._max_size:
            self._history.pop(0)
    
    def get_history(self) -> List[Calculation]:
        """
        Get the full calculation history.
        
        Returns:
            List of calculations
        """
        return self._history.copy()
    
    def get_last_calculation(self) -> Optional[Calculation]:
        """
        Get the most recent calculation.
        
        Returns:
            The last calculation or None if history is empty
        """
        if not self._history:
            return None
        return self._history[-1]
    
    def clear_history(self) -> None:
        """Clear all calculation history."""
        self._history.clear()
    
    def get_count(self) -> int:
        """
        Get the number of calculations in history.
        
        Returns:
            Number of calculations
        """
        return len(self._history)
    
    def save_to_csv(self, filepath: str) -> None:
        """
        Save calculation history to a CSV file using pandas.
        
        Args:
            filepath: Path to the CSV file
            
        Raises:
            HistoryError: If saving fails
        """
        if not self._history:
            raise HistoryError("No history to save")
        
        try:
            # Convert calculations to list of dictionaries
            data = [calc.to_dict() for calc in self._history]
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        except Exception as e:
            raise HistoryError(f"Failed to save history to CSV: {str(e)}")
    
    def load_from_csv(self, filepath: str) -> None:
        """
        Load calculation history from a CSV file using pandas.
        
        Args:
            filepath: Path to the CSV file
            
        Raises:
            HistoryError: If loading fails
        """
        try:
            # Read CSV into DataFrame
            df = pd.read_csv(filepath)
            
            # Clear existing history
            self._history.clear()
            
            # Convert each row back to a Calculation object
            for _, row in df.iterrows():
                try:
                    # Create operation from factory
                    operation = OperationFactory.create_operation(row['operation'])
                    
                    # Create calculation
                    calc = Calculation(operation, float(row['operand_a']), float(row['operand_b']))
                    
                    # Set result and timestamp
                    calc.result = float(row['result'])
                    calc.timestamp = pd.to_datetime(row['timestamp'])
                    
                    # Add to history
                    self._history.append(calc)
                except Exception as e:
                    # Skip invalid rows but continue loading
                    continue
            
            # Enforce max size
            if len(self._history) > self._max_size:
                self._history = self._history[-self._max_size:]
                
        except FileNotFoundError:
            raise HistoryError(f"History file not found: {filepath}")
        except Exception as e:
            raise HistoryError(f"Failed to load history from CSV: {str(e)}")
    
    def __str__(self) -> str:
        """Return string representation of history."""
        if not self._history:
            return "No calculations in history"
        
        lines = ["Calculation History:"]
        for i, calc in enumerate(self._history, 1):
            lines.append(f"{i}. {calc}")
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """Return detailed representation of history."""
        return f"CalculationHistory(count={len(self._history)}, max_size={self._max_size})""""
History management for calculator calculations.
Handles storing, saving, and loading calculation history using pandas.
"""

import pandas as pd
from datetime import datetime
from typing import List, Optional
from app.calculation import Calculation
from app.operations import OperationFactory
from app.exceptions import HistoryError


class CalculationHistory:
    """Manages the history of calculations."""
    
    def __init__(self, max_size: int = 100):
        """
        Initialize calculation history.
        
        Args:
            max_size: Maximum number of calculations to store
        """
        self._history: List[Calculation] = []
        self._max_size = max_size
    
    def add_calculation(self, calculation: Calculation) -> None:
        """
        Add a calculation to history.
        
        Args:
            calculation: The calculation to add
        """
        self._history.append(calculation)
        
        # Remove oldest if exceeding max size
        if len(self._history) > self._max_size:
            self._history.pop(0)
    
    def get_history(self) -> List[Calculation]:
        """
        Get the full calculation history.
        
        Returns:
            List of calculations
        """
        return self._history.copy()
    
    def get_last_calculation(self) -> Optional[Calculation]:
        """
        Get the most recent calculation.
        
        Returns:
            The last calculation or None if history is empty
        """
        if not self._history:
            return None
        return self._history[-1]
    
    def clear_history(self) -> None:
        """Clear all calculation history."""
        self._history.clear()
    
    def get_count(self) -> int:
        """
        Get the number of calculations in history.
        
        Returns:
            Number of calculations
        """
        return len(self._history)
    
    def save_to_csv(self, filepath: str) -> None:
        """
        Save calculation history to a CSV file using pandas.
        
        Args:
            filepath: Path to the CSV file
            
        Raises:
            HistoryError: If saving fails
        """
        if not self._history:
            raise HistoryError("No history to save")
        
        try:
            # Convert calculations to list of dictionaries
            data = [calc.to_dict() for calc in self._history]
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        except Exception as e:
            raise HistoryError(f"Failed to save history to CSV: {str(e)}")
    
    def load_from_csv(self, filepath: str) -> None:
        """
        Load calculation history from a CSV file using pandas.
        
        Args:
            filepath: Path to the CSV file
            
        Raises:
            HistoryError: If loading fails
        """
        try:
            # Read CSV into DataFrame
            df = pd.read_csv(filepath)
            
            # Clear existing history
            self._history.clear()
            
            # Convert each row back to a Calculation object
            for _, row in df.iterrows():
                try:
                    # Create operation from factory
                    operation = OperationFactory.create_operation(row['operation'])
                    
                    # Create calculation
                    calc = Calculation(operation, float(row['operand_a']), float(row['operand_b']))
                    
                    # Set result and timestamp
                    calc.result = float(row['result'])
                    calc.timestamp = pd.to_datetime(row['timestamp'])
                    
                    # Add to history
                    self._history.append(calc)
                except Exception as e:
                    # Skip invalid rows but continue loading
                    continue
            
            # Enforce max size
            if len(self._history) > self._max_size:
                self._history = self._history[-self._max_size:]
                
        except FileNotFoundError:
            raise HistoryError(f"History file not found: {filepath}")
        except Exception as e:
            raise HistoryError(f"Failed to load history from CSV: {str(e)}")
    
    def __str__(self) -> str:
        """Return string representation of history."""
        if not self._history:
            return "No calculations in history"
        
        lines = ["Calculation History:"]
        for i, calc in enumerate(self._history, 1):
            lines.append(f"{i}. {calc}")
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """Return detailed representation of history."""
        return f"CalculationHistory(count={len(self._history)}, max_size={self._max_size})"
