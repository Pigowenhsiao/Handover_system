"""
Lightweight logger helper.
Provides a get_logger function to align with task expectations.
"""
import logging


def get_logger(name: str = "handover-system") -> logging.Logger:
    """Return a logger with basic configuration."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


__all__ = ["get_logger"]
