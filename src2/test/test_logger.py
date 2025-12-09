import pytest
from utils.logger import Logger
import os

class TestLogger:
    """Tests para el Logger Singleton"""
    
    def test_singleton_pattern(self):
        """Test: Logger es singleton"""
        logger1 = Logger()
        logger2 = Logger()
        assert logger1 is logger2
    
    def test_logger_initialization(self, test_logger):
        """Test: Logger se inicializa correctamente"""
        assert test_logger.logger is not None
        assert test_logger.logger.name == 'DeepLearningAPI'
    
    def test_log_methods(self, test_logger, caplog):
        """Test: Métodos de logging funcionan"""
        test_logger.info("Info message")
        test_logger.warning("Warning message")
        test_logger.error("Error message")
        
        assert "Info message" in caplog.text
        assert "Warning message" in caplog.text
        assert "Error message" in caplog.text
    
    def test_log_file_creation(self, test_logger):
        """Test: Archivo de log se crea"""
        assert os.path.exists('logs')
        log_files = os.listdir('logs')
        assert len(log_files) > 0