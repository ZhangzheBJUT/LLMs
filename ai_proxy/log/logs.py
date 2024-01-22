import logging
import os
from typing import Any

from singleton import Singleton
from log.json_handler import JsonFileHandler, JsonFormatter

class Logger(metaclass=Singleton):
    """
    Logger that handle titles in different colors.
    Outputs logs in console, activity.log, and errors.log
    For console handler: simulates typing
    """

    def __init__(self):
        # create log directory if it doesn't exist
        this_files_dir_path = os.path.dirname(__file__)
        log_dir = os.path.join(this_files_dir_path, "../logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = "activity.log"
        error_file = "error.log"

        # Create a handler for console without typing simulation
        self.console_handler = ConsoleHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(logging.Formatter("%(title)s %(message)s"))

        # Info handler in activity.log
        self.file_handler = logging.FileHandler(
            os.path.join(log_dir, log_file), "a", "utf-8"
        )
        self.file_handler.setLevel(logging.DEBUG)
        info_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(title)s %(message)s"
        )
        self.file_handler.setFormatter(info_formatter)

        # Error handler error.log
        error_handler = logging.FileHandler(
            os.path.join(log_dir, error_file), "a", "utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(title)s"))

        self.logger = logging.getLogger("LOGGER")
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(error_handler)
        self.logger.setLevel(logging.DEBUG)

        self.json_logger = logging.getLogger("JSON_LOGGER")
        self.json_logger.addHandler(self.file_handler)
        self.json_logger.addHandler(error_handler)
        self.json_logger.setLevel(logging.DEBUG)

        self.speak_mode = False
        self.chat_plugins = []

    def debug(self, message, title="") -> None:
        self._log(title, message, level=logging.DEBUG)

    def info(self, message, title="",) -> None:
        self._log(title, message, level=logging.INFO)

    def warn(self, message, title=""):
        self._log(title, message, logging.WARN)

    def error(self, title, message=""):
        self._log(title, message, logging.ERROR)

    def _log(self, title: str = "", message: str = "",level=logging.INFO,):
        if message:
            if isinstance(message, list):
                message = " ".join(message)
        self.logger.log(
            level, message, extra={"title": str(title)}
        )

    def set_level(self, level):
        self.logger.setLevel(level)

    def log_json(self, data: Any, file_name: str) -> None:
        # Define log directory
        this_files_dir_path = os.path.dirname(__file__)
        log_dir = os.path.join(this_files_dir_path, "../logs")

        # Create a handler for JSON files
        json_file_path = os.path.join(log_dir, file_name)
        json_data_handler = JsonFileHandler(json_file_path)
        json_data_handler.setFormatter(JsonFormatter())

        # Log the JSON data using the custom file handler
        self.json_logger.addHandler(json_data_handler)
        self.json_logger.debug(data)
        self.json_logger.removeHandler(json_data_handler)

    def get_log_directory(self):
        this_files_dir_path = os.path.dirname(__file__)
        log_dir = os.path.join(this_files_dir_path, "../logs")
        return os.path.abspath(log_dir)


class ConsoleHandler(logging.StreamHandler):
    def emit(self, record) -> None:
        msg = self.format(record)
        try:
            print(msg)
        except Exception:
            self.handleError(record)

logger = Logger()
if __name__ == '__main__':
    logger.debug("debug ~ hello world")
    logger.info('info ~ hello world')
    logger.error('error ~ hello world')