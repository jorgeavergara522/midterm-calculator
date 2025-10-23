"""
Logging configuration for the calculator application.
"""

import logging
import os
from datetime import datetime


class Logger:
    """Manages logging for the calculator application."""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger if not already initialized."""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self, log_dir: str = "logs", log_file: str = "calculator.log"):
        """
        Set up the logger with file and console handlers.
        
        Args:
            log_dir: Directory to store log files
            log_file: Name of the log file
        """
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self._logger = logging.getLogger('calculator')
        self._logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self._logger.handlers:
            return
        
        # Create file handler
        log_path = os.path.join(log_dir, log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log an info message."""
        self._logger.info(message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self._logger.warning(message)
    
    def error(self, message: str):
        """Log an error message."""
        self._logger.error(message)
    
    def debug(self, message: str):
        """Log a debug message."""
        self._logger.debug(message)
    
    def log_calculation(self, operation: str, operand_a: float, operand_b: float, result: float):
        """
        Log a calculation with details.
        
        Args:
            operation: Name of the operation
            operand_a: First operand
            operand_b: Second operand
            result: Result of the calculation
        """
        self.info(f"Calculation: {operand_a} {operation} {operand_b} = {result}")"""
Logging configuration for the calculator application.
"""

import logging
import os
from datetime import datetime


class Logger:
    """Manages logging for the calculator application."""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger if not already initialized."""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self, log_dir: str = "logs", log_file: str = "calculator.log"):
        """
        Set up the logger with file and console handlers.
        
        Args:
            log_dir: Directory to store log files
            log_file: Name of the log file
        """
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self._logger = logging.getLogger('calculator')
        self._logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self._logger.handlers:
            return
        
        # Create file handler
        log_path = os.path.join(log_dir, log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log an info message."""
        self._logger.info(message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self._logger.warning(message)
    
    def error(self, message: str):
        """Log an error message."""
        self._logger.error(message)
    
    def debug(self, message: str):
        """Log a debug message."""
        self._logger.debug(message)
    
    def log_calculation(self, operation: str, operand_a: float, operand_b: float, result: float):
        """
        Log a calculation with details.
        
        Args:
            operation: Name of the operation
            operand_a: First operand
            operand_b: Second operand
            result: Result of the calculation
        """
        self.info(f"Calculation: {operand_a} {operation} {operand_b} = {result}")
