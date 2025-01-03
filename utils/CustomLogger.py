import logging
import os
from datetime import datetime

class customLogger:
    def __init__(self, log_folder='Log', log_level=logging.DEBUG):
        self.log_folder = log_folder
        self.log_level = log_level
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)
        self._setup_log_directory()
        self._setup_file_handler()
        self._setup_console_handler()

    def _setup_log_directory(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    def _setup_file_handler(self):
        log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log')
        file_handler = logging.FileHandler(os.path.join(self.log_folder, log_filename))
        file_handler.setLevel(self.log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _setup_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

# Usage example
if __name__ == "__main__":
    custom_logger = customLogger()
    logger = custom_logger.get_logger()
    logger.info("This is an info message")
    logger.error("This is an error message")