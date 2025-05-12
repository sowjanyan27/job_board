import logging
import os

def get_logger(module_name: str, log_file: str = None):
    # Create log directory if it doesn't exist
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)

    # Initialize logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding multiple handlers to the logger (i.e., duplicate logs)
    if not logger.handlers:
        # Default to "app.log" if no log file is provided
        log_file = log_file or f"{log_dir}/{module_name}.log"
        file_handler = logging.FileHandler(log_file, mode='a')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
