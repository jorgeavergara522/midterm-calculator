
"""
Calculation class to represent a single calculation.
"""

from datetime import datetime
from app.operations import Operation


class Calculation:
    """Represents a single calculation with operation, operands, and result."""
    
    def __init__(self, operation: Operation, operand_a: float, operand_b: float):
        """
        Initialize a calculation.
        
        Args:
            operation: The operation to perform
            operand_a: First operand
            operand_b: Second operand
        """
        self.operation = operation
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.result = None
        self.timestamp = datetime.now()
    
    def execute(self) -> float:
        """
        Execute the calculation and store the result.
        
        Returns:
            The result of the calculation
        """
        self.result = self.operation.execute(self.operand_a, self.operand_b)
        return self.result
    
    def __str__(self) -> str:
        """Return string representation of the calculation."""
        operation_name = self.operation.__class__.__name__.replace('Operation', '').lower()
        if self.result is not None:
            return f"{self.operand_a} {self.operation.get_symbol()} {self.operand_b} = {self.result}"
        return f"{self.operand_a} {self.operation.get_symbol()} {self.operand_b}"
    
    def __repr__(self) -> str:
        """Return detailed representation of the calculation."""
        return f"Calculation({self.operation.__class__.__name__}, {self.operand_a}, {self.operand_b}, result={self.result})"
    
    def to_dict(self) -> dict:
        """
        Convert calculation to dictionary for serialization.
        
        Returns:
            Dictionary representation of the calculation
        """
        operation_name = self.operation.__class__.__name__.replace('Operation', '').lower()
        return {
            'operation': operation_name,
            'operand_a': self.operand_a,
            'operand_b': self.operand_b,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
