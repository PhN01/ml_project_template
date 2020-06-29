import os
import colorlog
import logging
import datetime
import sys


def make_dirs_checked(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def get_logger(log_path=None):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(message)s",
        log_colors={
            "DEBUG": "bold_cyan",
            "INFO": "bold_green",
            "WARNING": "bold_yellow",
            "ERROR": "bold_red",
            "CRITICAL": "white,bg_red",
        },
    )

    # Logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
    )
    stream_handler.setFormatter(console_formatter)
    logger.addHandler(stream_handler)

    # Logging to a file
    if not log_path is None:
        make_dirs_checked(log_path)

        ts = datetime.datetime.now().strftime("%Y%m%d-T%H:%M:%S")
        log_file = f"{'.'.join(sys.argv[0].split('/')[-3:])}-{ts}.log"
        file_handler = logging.FileHandler(
            f"{log_path}/{log_file}", mode="a", encoding=None, delay=False
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
        )
        logger.addHandler(file_handler)

    return logger
