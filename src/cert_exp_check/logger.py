import logging
import sys
from colorama import Fore, Style


def setup_logger(log_level='INFO', log_file=None):
    """
    Sets up a single logger for the entire app with two different formatters:
    - Console logs: Simple and clean, with colored output but no timestamps.
    - File logs: Detailed with timestamps, module names, and log levels.

    :param log_level: Logging level as a string ('INFO', 'DEBUG', 'ERROR', etc.).
    :param log_file: Optional path to a log file.
    :return: Configured logger instance.
    """
    # Convert log level string to logging constant
    log_level = getattr(logging, log_level.upper(), logging.INFO)

    # Get root logger (single logger for all modules)
    logger = logging.getLogger("cert_exp_check")
    logger.setLevel(log_level)

    # Prevent duplicate log entries
    if logger.hasHandlers():
        logger.handlers.clear()

    # ✅ Console log formatter (simple, no timestamp)
    console_formatter = logging.Formatter('%(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(ColorFormatter(console_formatter))
    logger.addHandler(console_handler)

    # ✅ File log formatter (detailed, with timestamp and module names)
    if log_file:
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


class ColorFormatter(logging.Formatter):
    """Custom formatter to add color to console log messages based on their severity."""
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def __init__(self, formatter):
        super().__init__()
        self.formatter = formatter

    def format(self, record):
        log_msg = self.formatter.format(record)
        color = self.COLORS.get(record.levelno, Style.RESET_ALL)
        return color + log_msg + Style.RESET_ALL
