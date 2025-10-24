"""
Main Calculator class with REPL interface and Observer pattern.
"""

from abc import ABC, abstractmethod
from typing import List
from app.calculation import Calculation
from app.operations import OperationFactory
from app.history import CalculationHistory
from app.calculator_memento import CalculatorCaretaker
from app.calculator_config import CalculatorConfig
from app.logger import Logger
from app.input_validators import validate_number, validate_in_range
from app.exceptions import OperationError, ValidationError, HistoryError


# Observer Pattern Implementation
class CalculationObserver(ABC):
    """Abstract observer for calculation events."""
    
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """Called when a new calculation is performed."""
        pass


class LoggingObserver(CalculationObserver):
    """Observer that logs each calculation."""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def update(self, calculation: Calculation) -> None:
        """Log the calculation details."""
        self.logger.log_calculation(
            calculation.operation.__class__.__name__.replace('Operation', '').lower(),
            calculation.operand_a,
            calculation.operand_b,
            calculation.result
        )


class AutoSaveObserver(CalculationObserver):
    """Observer that automatically saves history to CSV."""
    
    def __init__(self, history: CalculationHistory, filepath: str):
        self.history = history
        self.filepath = filepath
    
    def update(self, calculation: Calculation) -> None:
        """Auto-save history to CSV file."""
        try:
            if self.history.get_count() > 0:
                self.history.save_to_csv(self.filepath)
        except HistoryError:
            pass  # Silently handle auto-save errors


class Calculator:
    """Main calculator class with REPL interface."""
    
    def __init__(self):
        """Initialize the calculator with all components."""
        self.config = CalculatorConfig()
        self.logger = Logger()
        self.history = CalculationHistory(max_size=self.config.max_history_size)
        self.caretaker = CalculatorCaretaker()
        self.observers: List[CalculationObserver] = []
        
        # Register observers
        self.register_observer(LoggingObserver(self.logger))
        if self.config.auto_save:
            self.register_observer(AutoSaveObserver(self.history, self.config.history_file))
        
        self.logger.info("Calculator initialized")
    
    def register_observer(self, observer: CalculationObserver) -> None:
        """Register an observer to receive calculation updates."""
        self.observers.append(observer)
    
    def notify_observers(self, calculation: Calculation) -> None:
        """Notify all observers of a new calculation."""
        for observer in self.observers:
            observer.update(calculation)
    
    def perform_calculation(self, operation_name: str, operand_a: float, operand_b: float) -> float:
        """
        Perform a calculation and update history.
        
        Args:
            operation_name: Name of the operation
            operand_a: First operand
            operand_b: Second operand
            
        Returns:
            Result of the calculation
        """
        # Validate inputs
        operand_a = validate_number(operand_a, "operand_a")
        operand_b = validate_number(operand_b, "operand_b")
        validate_in_range(operand_a, self.config.max_input_value, "operand_a")
        validate_in_range(operand_b, self.config.max_input_value, "operand_b")
        
        # Save state before performing calculation (for undo)
        self.caretaker.save_state(self.history.get_history())
        
        # Create and execute calculation
        operation = OperationFactory.create_operation(operation_name)
        calculation = Calculation(operation, operand_a, operand_b)
        result = calculation.execute()
        
        # Round result to configured precision
        result = round(result, self.config.precision)
        calculation.result = result
        
        # Add to history
        self.history.add_calculation(calculation)
        
        # Notify observers
        self.notify_observers(calculation)
        
        return result
    
    def undo(self) -> None:
        """Undo the last calculation."""
        restored_history = self.caretaker.undo(self.history.get_history())
        self.history._history = restored_history
        self.logger.info("Undo performed")
    
    def redo(self) -> None:
        """Redo the last undone calculation."""
        restored_history = self.caretaker.redo()
        self.history._history = restored_history
        self.logger.info("Redo performed")
    
    def show_history(self) -> None:
        """Display calculation history."""
        print("\n" + str(self.history))
    
    def clear_history(self) -> None:
        """Clear all calculation history."""
        self.history.clear_history()
        self.caretaker.clear()
        self.logger.info("History cleared")
        print("History cleared")
    
    def save_history(self) -> None:
        """Manually save history to CSV."""
        try:
            self.history.save_to_csv(self.config.history_file)
            self.logger.info(f"History saved to {self.config.history_file}")
            print(f"History saved to {self.config.history_file}")
        except HistoryError as e:
            print(f"Error: {e}")
    
    def load_history(self) -> None:
        """Load history from CSV."""
        try:
            self.history.load_from_csv(self.config.history_file)
            self.logger.info(f"History loaded from {self.config.history_file}")
            print(f"History loaded from {self.config.history_file}")
        except HistoryError as e:
            print(f"Error: {e}")
    
    def show_help(self) -> None:
        """Display available commands."""
        help_text = """
Available Commands:
==================
Arithmetic Operations:
  add <a> <b>       - Add two numbers
  subtract <a> <b>  - Subtract b from a
  multiply <a> <b>  - Multiply two numbers
  divide <a> <b>    - Divide a by b
  power <a> <b>     - Raise a to the power of b
  root <a> <b>      - Calculate the bth root of a
  modulus <a> <b>   - Calculate a modulo b
  int_divide <a> <b> - Integer division of a by b
  percent <a> <b>   - Calculate percentage (a/b * 100)
  abs_diff <a> <b>  - Absolute difference between a and b

History Commands:
  history           - Show calculation history
  clear             - Clear calculation history
  undo              - Undo last calculation
  redo              - Redo last undone calculation
  save              - Save history to CSV file
  load              - Load history from CSV file

Other Commands:
  help              - Show this help message
  exit              - Exit the calculator
        """
        print(help_text)
    
    def repl(self) -> None:
        """Run the Read-Eval-Print Loop (REPL) interface."""
        print("Calculator REPL - Type 'help' for available commands")
        self.logger.info("REPL started")
        
        while True:
            try:
                user_input = input("> ").strip().lower()
                
                if not user_input:
                    continue
                
                parts = user_input.split()
                command = parts[0]
                
                # Exit command
                if command == "exit":
                    print("Goodbye!")
                    self.logger.info("Calculator exiting")
                    break
                
                # Help command
                elif command == "help":
                    self.show_help()
                
                # History commands
                elif command == "history":
                    self.show_history()
                
                elif command == "clear":
                    self.clear_history()
                
                elif command == "undo":
                    try:
                        self.undo()
                        print("Undo successful")
                        self.show_history()
                    except HistoryError as e:
                        print(f"Error: {e}")
                
                elif command == "redo":
                    try:
                        self.redo()
                        print("Redo successful")
                        self.show_history()
                    except HistoryError as e:
                        print(f"Error: {e}")
                
                elif command == "save":
                    self.save_history()
                
                elif command == "load":
                    self.load_history()
                
                # Arithmetic operations
                elif command in OperationFactory.get_available_operations():
                    if len(parts) != 3:
                        print(f"Error: {command} requires exactly 2 numbers")
                        print(f"Usage: {command} <number1> <number2>")
                        continue
                    
                    try:
                        result = self.perform_calculation(command, parts[1], parts[2])
                        print(f"Result: {result}")
                    except (OperationError, ValidationError) as e:
                        print(f"Error: {e}")
                        self.logger.error(str(e))
                
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
            
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.logger.error(f"Unexpected error: {e}")


def main():
    """Main entry point for the calculator application."""
    calculator = Calculator()
    calculator.repl()


if __name__ == "__main__":
    main()
