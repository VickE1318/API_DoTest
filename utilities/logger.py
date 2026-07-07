import logging
import os
import sys

_logger_initialized = True

def setup_logger(level_name: str = "INFO"):
    global _logger_initialized
    if _logger_initialized:
        return
    os.makedirs("logs", exist_ok=True)
    numeric_level = getattr(logging, level_name.upper(), logging.INFO)
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    targets = logging.StreamHandler(sys.stdout), logging.FileHandler('logs/execution.log')
    logging.basicConfig(
        level = numeric_level,
        encoding='utf-8', 
        format=log_format,
        handlers=targets,
        force=True)
    _logger_initialized = True

def get_logger(module_name: str) -> logging.Logger:
    return logging.getLogger(f"API_DoTest.{module_name}")
