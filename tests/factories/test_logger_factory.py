import logging
from unittest.mock import MagicMock
from src.factories.logger_factory import LoggerFactory

def test_create_logger_configures_providers():
    # Arrange
    factory = LoggerFactory()
    mock_provider = MagicMock() # Create a fake provider
    factory.add_provider(mock_provider)
    
    # Act
    logger = factory.create_logger("test_category")
    
    # Assert
    # Verify the provider was called
    mock_provider.configure_logger.assert_called_once_with(logger)
    # Verify propagation is disabled
    assert logger.propagate is False

def test_dispose_clears_providers():
    # Arrange
    factory = LoggerFactory()
    mock_provider = MagicMock()
    factory.add_provider(mock_provider)
    
    # Act
    factory.dispose()
    
    # Assert
    mock_provider.dispose.assert_called_once()
    assert len(factory._providers) == 0

def test_handler_clearing():
    # Arrange
    factory = LoggerFactory()
    logger = logging.getLogger("test_clear")
    logger.addHandler(logging.StreamHandler()) # Add a dummy handler
    
    # Act
    factory.create_logger("test_clear")
    
    # Assert
    assert len(logger.handlers) == 0