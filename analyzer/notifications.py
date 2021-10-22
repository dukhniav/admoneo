import queue
import threading
from os import path

import apprise
import logging

from analyzer import __logger__
from analyzer.configuration.configuration import Config

logger = logging.getLogger(__logger__)


class NotificationHandler:
    def __init__(self, config: Config, enabled=True):
        self.config = config
        if self.config.TGRAM_ENABLED:
            self.apobj = apprise.Apprise()
            apprise_config = apprise.AppriseConfig()
            apprise_config.add(self.config)
            self.apobj.add(apprise_config)
            self.queue = queue.Queue()
            self.start_worker()
            self.enabled = True
        else:
            self.enabled = False
        logger.debug("Starting NotificationHandler...")

    def start_worker(self):
        threading.Thread(target=self.process_queue, daemon=True).start()

    def process_queue(self):
        while True:
            message, attachments = self.queue.get()

            if attachments:
                self.apobj.notify(body=message, attach=attachments)
            else:
                self.apobj.notify(body=message)
            self.queue.task_done()

    def send_notification(self, message, attachments=None):
        if self.enabled:
            self.queue.put((message, attachments or []))
