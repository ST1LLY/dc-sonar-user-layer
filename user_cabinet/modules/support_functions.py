"""
Support functions for the main logic

Author:
    Konstantin S. (https://github.com/ST1LLY)
"""
import json
import logging
import traceback
from logging.handlers import RotatingFileHandler
from typing import Any

from colorlog import ColoredFormatter


def dict_to_json_bytes(converting_dict: dict[str, Any]) -> bytes:
    """
    Convert dict to json and output bytes
    """
    return (json.dumps(converting_dict, ensure_ascii=False)).encode('utf-8')


def init_custome_logger(
    all_log_file_path: str,
    error_log_file_path: str,
    logging_level: str = 'DEBUG',
    console_format: str = '%(process)s %(thread)s: %(asctime)s - %(filename)s:%(lineno)d - %(funcName)s -%(log_color)s'
    ' %(levelname)s %(reset)s - %(message)s',
    file_format: str = '%(process)s %(thread)s: %(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s -'
    ' %(message)s',
) -> logging.Logger:
    """
    Creating custom logger
    """
    # Setting console output handler

    stream_formatter = ColoredFormatter(console_format)
    logging_level_num = 20 if logging_level == 'INFO' else 10
    max_bytes = 20 * 1024 * 1024  # 20MB максимальный размер лог файла
    backup_count = 10

    # Setting log file output handler
    file_handler = RotatingFileHandler(
        filename=all_log_file_path, mode='a', maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(fmt=file_format))
    file_handler.setLevel(logging_level_num)

    # Setting error log file output handler
    error_file_handler = RotatingFileHandler(
        filename=error_log_file_path, mode='a', maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
    )
    error_file_handler.setFormatter(logging.Formatter(fmt=file_format))
    error_file_handler.setLevel(logging.WARNING)

    # Set ours handlers to root handler
    logging.basicConfig(level=logging_level_num)

    logger = logging.getLogger()
    # Changing the output format of root stream handler
    logger.handlers[0].setFormatter(stream_formatter)

    # logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    return logger


def get_error_text(exc: Exception) -> str:
    """
    Get full text of the Exception
    """
    error_traceback_format = traceback.format_exc()
    return f'{exc}\n{error_traceback_format}'

def get_file_text(path: str) -> str:
    """
    Getting text from file
    Args:
        path (str): file path

    Returns:
        str: text
    """
    with open(path, 'r', encoding='utf-8') as file:
        text_template = file.read()
    return text_template