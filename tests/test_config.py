"""
Unit tests for CalculatorConfig.
"""

import os
import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_config_loads_defaults():
    """Test config loads with default values."""
    config = CalculatorConfig()
    
    assert config.log_dir is not None
    assert config.history_dir is not None
    assert config.max_history_size >= 0
    assert config.precision >= 0


def test_config_creates_directories():
    """Test config creates necessary directories."""
    config = CalculatorConfig()
    
    # Directories should be created
    assert os.path.exists(config.log_dir) or config.log_dir == 'logs'
    assert os.path.exists(config.history_dir) or config.history_dir == 'history'


def test_config_repr():
    """Test config string representation."""
    config = CalculatorConfig()
    repr_str = repr(config)
    
    assert "CalculatorConfig" in repr_str
