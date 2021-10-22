import logging.handlers

from .notifications import NotificationHandler


class Logger:

    Logger = None
    NotificationHandler = None

    def __init__(self, config, logging_service="analyzer", enable_notifications=True):
        # Logger setup
        self.Logger = logging.getLogger(f"{logging_service}_logger")
        self.Logger.setLevel(logging.DEBUG)
        self.Logger.propagate = False
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # default is "logs/crypto_trading.log"
        fh = logging.FileHandler(f"./logs/{logging_service}.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.Logger.addHandler(fh)

        # logging to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.Logger.addHandler(ch)
        self.config = config

        # notification handler
        self.NotificationHandler = NotificationHandler(
            self.config, enable_notifications)

    def log(self, message, level="info", notification=True):

        if level == "info":
            self.Logger.info(message)
        elif level == "warning":
            self.Logger.warning(message)
        elif level == "error":
            self.Logger.error(message)
        elif level == "debug":
            self.Logger.debug(message)

        if notification and self.NotificationHandler.enabled:
            self.NotificationHandler.send_notification(str(message))

    def info(self, message, notification=True):
        self.log(message, "info", notification)

    def warning(self, message, notification=True):
        self.log(message, "warning", notification)

    def error(self, message, notification=True):
        self.log(message, "error", notification)

    def debug(self, message, notification=False):
        self.log(message, "debug", notification)

    def update_logger(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S', filename='Logs/testGene.log', filemode='w')
