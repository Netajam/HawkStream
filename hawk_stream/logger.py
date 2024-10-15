import logging


class AppLogger:
    def __init__(self, log_name="app", log_level=logging.DEBUG):  
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        if not self.logger.hasHandlers():
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            log_file = f"{log_name}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

app_logger = AppLogger(log_name="hawkstream").get_logger()
