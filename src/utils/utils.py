import logging
import os
import sys
from datetime import datetime
from typing import Tuple, Union

import colorlog


def make_dirs_checked(directory: str) -> None:
    """If not exists yet: create directory (and all non-existent dirs in its path)"""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def split_path(filepath: str) -> Tuple[str, str, str]:
    """Split a filepath into its directory path, basename and file extension"""
    directory, filename = os.path.split(filepath)
    basename, extension = os.path.splitext(filename)
    return (directory, basename, extension)


def make_path(path_tup: Union[str, Tuple]) -> str:
    if isinstance(path_tup, tuple):
        if len(path_tup) == 2:
            dir, file = path_tup
            path = os.path.join(dir, file)
        elif len(path_tup) == 3:
            dir, file, ext = path_tup
            path = os.path.join(dir, file + ext)
    else:
        path = path_tup

    return path


def get_logger(log_path: Union[str, None] = None, force: bool = True) -> logging.Logger:
    """[summary]

    Args:
        log_path (Union[str, None], optional): [description]. Defaults to None.
        force (bool, optional): [description]. Defaults to True.

    Returns:
        logging.Logger: [description]
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # define colorlog
    stream_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(threadName)s] [%(levelname)s]    "
        "%(reset)s%(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red",
        },
    )

    # Logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    # logging to file
    if log_path is not None:
        # check for existing file handlers:
        for handler in logger.handlers:
            if type(handler) is logging.FileHandler:
                if force:
                    logger.info("Removing existing FileHandler:")
                    logger.info(f"{getattr(handler,'baseFilename')}")
                    logger.removeHandler(handler)
                else:
                    logger.info("Existing FileHandler found:")
                    logger.info(f"Logging to {getattr(handler,'baseFilename')} instead")

        # create log_path directory
        make_dirs_checked(log_path)

        # create log filename
        ts = datetime.now().strftime("%Y%m%d-T%H:%M:%S")
        if "__file__" in locals():
            if "src" in sys.argv[0]:
                ts = datetime.now().strftime("%Y%m%d-T%H:%M:%S")
                path_split = sys.argv[0].split("/")
                src_idx = path_split.index("src")
                filename = f"{'.'.join(path_split[src_idx:])}-{ts}.log"
            else:
                filename = f"{__file__}-{ts}.log"
        else:
            filename = f"terminal-{ts}.log"

        # create filehandler
        file_handler = logging.FileHandler(
            f"{log_path}/{filename}", mode="a", encoding=None, delay=False
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s"
            )
        )
        logger.addHandler(file_handler)

    return logger
