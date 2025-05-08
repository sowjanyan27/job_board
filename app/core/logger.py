# import logging
#
# def setup_logger():
#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s",
#         filename="app.log",
#         filemode="a",
#     )
#     return logging.getLogger("job_board_logger")
#
# logger = setup_logger()
import logging
import os


def get_logger(module_name: str):
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(f"{log_dir}/{module_name}.log", mode='a')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
