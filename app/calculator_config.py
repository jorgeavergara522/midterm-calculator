"""
Configuration management for the calculator application.
"""

import os
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages configuration settings for the calculator."""
    
    def __init__(self):
        """Initialize configuration by loading from .env file."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Load configuration with defaults
        self.log_dir = os.getenv('CALCULATOR_LOG_DIR', 'logs')
        self.history_dir = os.getenv('CALCULATOR_HISTORY_DIR', 'history')
        self.max_history_size = self._get_int('CALCULATOR_MAX_HISTORY_SIZE', 100)
        self.auto_save = self._get_bool('CALCULATOR_AUTO_SAVE', True)
        self.precision = self._get_int('CALCULATOR_PRECISION', 2)
        self.max_input_value = self._get_float('CALCULATOR_MAX_INPUT_VALUE', 1000000.0)
        self.default_encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
        self.log_file = os.getenv('CALCULATOR_LOG_FILE', f'{self.log_dir}/calculator.log')
        self.history_file = os.getenv('CALCULATOR_HISTORY_FILE', 
                                     f'{self.history_dir}/calculation_history.csv')
        
        # Create necessary directories
        self._create_directories()
    
    def _get_int(self, key: str, default: int) -> int:
        """
        Get an integer value from environment variables.
        
        Args:
            key: Environment variable key
            default: Default value if key not found or invalid
            
        Returns:
            Integer value
        """
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            raise ConfigurationError(f"Invalid integer value for {key}: {value}")
    
    def _get_float(self, key: str, default: float) -> float:
        """
        Get a float value from environment variables.
        
        Args:
            key: Environment variable key
            default: Default value if key not found or invalid
            
        Returns:
            Float value
        """
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            raise ConfigurationError(f"Invalid float value for {key}: {value}")
    
    def _get_bool(self, key: str, default: bool) -> bool:
        """
        Get a boolean value from environment variables.
        
        Args:
            key: Environment variable key
            default: Default value if key not found
            
        Returns:
            Boolean value
        """
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
    
    def __repr__(self) -> str:
        """Return string representation of configuration."""
        return (f"CalculatorConfig(log_dir='{self.log_dir}', "
                f"history_dir='{self.history_dir}', "
                f"max_history_size={self.max_history_size}, "
                f"precision={self.precision})")
        
        """
Configuration management for the calculator application.
"""

import os
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages configuration settings for the calculator."""
    
    def __init__(self):
        """Initialize configuration by loading from .env file."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Load configuration with defaults
        self.log_dir = os.getenv('CALCULATOR_LOG_DIR', 'logs')
        self.history_dir = os.getenv('CALCULATOR_HISTORY_DIR', 'history')
        self.max_history_size = self._get_int('CALCULATOR_MAX_HISTORY_SIZE', 100)
        self.auto_save = self._get_bool('CALCULATOR_AUTO_SAVE', True)
        self.precision = self._get_int('CALCULATOR_PRECISION', 2)
        self.max_input_value = self._get_float('CALCULATOR_MAX_INPUT_VALUE', 1000000.0)
        self.default_encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
        self.log_file = os.getenv('CALCULATOR_LOG_FILE', f'{self.log_dir}/calculator.log')
        self.history_file = os.getenv('CALCULATOR_HISTORY_FILE', 
                                     f'{self.history_dir}/calculation_history.csv')
        
        # Create necessary directories
        self._create_directories()
    
    def _get_int(self, key: str, default: int) -> int:
        """
        Get an integer value from environment variables.
        
        Args:
            key: Environment variable key
            default: Default value if key not found or invalid
            
        Returns:
            Integer value
        """
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            raise ConfigurationError(f"Invalid integer value for {key}: {value}")
    
    def _get_float(self, key: str, default: float) -> float:
        """
        Get a float value from environment variables.
        
        Args:
            key: Environment variable key
            default: Default value if key not found or invalid
            
        Returns:
            Float value
        """
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            raise ConfigurationError(f"Invalid float value for {key}: {value}")
    
    def _get_bool(self, key: str, default: bool) -> bool:
        """
        Get a boolean value from environment variables.
        
        Args:
            key: Environment variable key
            default: Default value if key not found
            
        Returns:
            Boolean value
        """
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
    
    def __repr__(self) -> str:
        """Return string representation of configuration."""
        return (f"CalculatorConfig(log_dir='{self.log_dir}', "
                f"history_dir='{self.history_dir}', "
                f"max_history_size={self.max_history_size}, "
                f"precision={self.precision})")
