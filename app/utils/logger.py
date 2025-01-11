<<<<<<< HEAD
# utils/__init__.py
from .logger import get_logger

=======
>>>>>>> 1057750b7e20d3b20fee5059f81006ae529d5914
# utils/logger.py
import logging
import sys
from typing import Any
from pathlib import Path
from loguru import logger

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging(log_file: str = "app.log") -> None:
    """Configure logging with loguru."""
    # Remove default logger
    logger.remove()

    # Configure loguru logger
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Add console handler
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True
    )
    
    # Add file handler
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    logger.add(
        log_path / log_file,
        format=log_format,
        level="DEBUG",
        rotation="1 day",
        retention="7 days",
        compression="zip"
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

def get_logger(name: str) -> Any:
    """Get a logger instance."""
    setup_logging()
    return logger.bind(name=name)