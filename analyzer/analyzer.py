"""
Analyzer bot
"""

from numpy import reciprocal
from analyzer.config.config import Config
from analyzer.database import Database
from analyzer.processor import Processor
from analyzer.scheduler import SafeScheduler
# from .notifications import Notifications
from analyzer.notifications import Telegram
from analyzer.utils_rpc.rpc import RPCHandler, RPC
from analyzer.utils_rpc.rpc_manager import RPCManager
from analyzer.enums import CommsMsgType

from .enums.state import State

from logging import getLogger

logger = getLogger(__name__)


class Analyzer:
    def __init__(self, config: Config):
        logger.info("Initializing Analyzer...")

        self.config = config
        self.initial_state = config.INITIAL_STATE
        self.state=State[self.initial_state.upper()]

        logger.info(f"Bot state is: {self.state}")
        if self.state == State.STOPPED:
            logger.warning("Bot has been stopped")


        # Initialize modules
        self.__init_schedule()
        self.__init_db()
        self.__init_rpc()
        if self.config.TGRAM_ENABLED:
            self.__init_notifications()
        self.__init_processor()

        if self.state != self.state.RUNNING:
            self.state=State.STOPPED
            logger.info("Bot is stopped, start from telegram")
            self.chatbot.send_msg("Bot is stopped, use /start")

        if self.config.TGRAM_NOTI == 'on':
            self.chatbot.send_msg({
            'type': CommsMsgType.STATUS,
            'status': "Initializing bot..."
        })

        self.coin_list = self.processor.coin_list

    def __init_rpc(self):
        logger.info("Initializing RPC Handler")
        # RPC runs in separate threads, can start handling external commands just after
        # initialization, even before Freqtradebot has a chance to start its throttling,
        # so anything in the Freqtradebot instance should be ready (initialized), including
        # the initial state of the bot.
        # Keep this at the end of this initialization method.
        self.rpc: RPC = RPC(self)

    def __init_db(self):
        logger.info("Initializing database...")
        self.db = Database(self.config)

    def __init_notifications(self):
        logger.info("Initialing chatbot...")
        self.chatbot = Telegram(self.rpc, self.config)

    def __init_processor(self):
        logger.info("Initializing processor...")
        self.processor=Processor(self.config, self.db, self.chatbot)

    def __init_schedule(self):
        logger.info("Initializing scheduler...")
        self.schedule=SafeScheduler()

    def send_update(self, msg):
        logger.warning("update not implemented")
        # self.chatbot.send_notification(msg)

    def prune_logs(self):
        logger.info("Purge logs")
