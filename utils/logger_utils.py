import logging

class Logger:
    """Logger utility. 
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._start_logger()
        return cls._instance

    def _start_logger(self):
        log_file = "logs/audit.log"
        log_level = logging.DEBUG

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log_info(self, message):
        """Informational. To be used for auditing user actions with the system i.e., functionality / usage, 
        especially in terms of data sets loaded, imported, exported, saved, manipulated etc. 

        Args:
            message (str): message to log.
        """
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        """For messages that don't require exception information Used more specificially for logging just error codes.
        Example usage:

        try: 
            # Some code that might raise an exception
        except Exception as e:
            logger.error(f"Error code: {e}")

        Args:
            message (str): message to log, e.g., error code
        """
        self.logger.error(message)

    def log_exception(self, message):
        """Logs the error message and automatically appends the traceback of the exception that occurred. 
        Useful when you want to capture detailed information about the exception, including the traceback, 
        to help with debugging.

        Args:
            message (str): message to log.
        """
        self.logger.exception(message)
