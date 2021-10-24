#!python3
import time
import logging
import sys

from typing import Any, List
from os import getpid

from analyzer import __version__, __name__
from analyzer import processor
from .config import Config
from .database import Database
from .scheduler import SafeScheduler
from analyzer.utils.exceptions import AnalyzerException, OperationalException
from analyzer.loggers import setup_logging_pre
from analyzer import loggers
from analyzer.processor import Processor
from analyzer.loader import Loader
from analyzer.communications.telegram_bot import TelegramBot
from analyzer.communications import utils
from analyzer.utils.enums.state import State

logger = logging.getLogger(__name__)


def main():
    """
    This function will initiate the bot and start the  loop.
    :return: None
    """

    return_code: Any = 1

    try:
        logger.info("Starting bot...")

        config = Config()
        setup_logging_pre()
        loggers.setup_logging(config)

        # Set initial bot state from config
        initial_state = config.INITIAL_STATE
        state = State[initial_state.upper(
        )] if initial_state else State.STOPPED

        loader = Loader(config)

        t_gram = TelegramBot(config)

        # Comms
        if config.TGRAM_TOKEN is None or config.TGRAM_CHAT_ID is None:
            utils.setup_telegram_constants()
        _heartbeat_interval = config.HEARTBEAT_INTERVAL
        _heartbeat_msg = 0

        db = Database(t_gram, loader, config)

        processor = Processor(loader, db, config)

        # comms = TelegramBot(config)

        # # APIs
        # binance = BinanceAPIManager(config, db)
        # if binance.enabled:
        #     logger.info("Binance API enabled...")
        #     config.BINANCE_ENABLED = True

        # manager = BinanceAPIManager(config, db, logger)
        # strategy = get_strategy(config.STRATEGY)
        # if strategy is None:
        #     logger.error("Invalid strategy name")
        #     return

        # trader = strategy(manager, db, logger, config)
        # logger.info(f"Strategy selected: {config.STRATEGY}")

        # logger.info("Setting approved coin list...")
        # # db.set_coins(config.SUPPORTED_COIN_LIST)
        # db.migrate_old_state()

        schedule = SafeScheduler()

        # schedule.every(60).seconds.do(processor.check_new_coins).tag("checking coins")
        # processor.check_new_coins()
        coin_list = processor.load_coin_list()
        processor.update_coin_data_from_list(coin_list)


        # schedule.every(1).minutes.do(trader.update_values).tag("updating value history")
        # schedule.every(1).minutes.do(db.prune_scout_history).tag("pruning scout history")
        # schedule.every(1).hours.do(db.prune_value_history).tag("pruning value history")

        while state == State.RUNNING:
            if _heartbeat_interval:
                now = time.time()
                if (now - _heartbeat_msg) > _heartbeat_interval:
                    logger.info(f"Bot heartbeat. PID={getpid()}, "
                                f"version='{__version__}', state='{state.name}'")
                    _heartbeat_msg = now
            schedule.run_pending()
            time.sleep(config.BOT_SLEEP_TIME)

    except SystemExit as e:  # pragma: no cover
        return_code = e
    except KeyboardInterrupt:
        logger.info('SIGINT received, aborting ...')
        return_code = 0
    except AnalyzerException as e:
        logger.error(str(e))
        return_code = 2
    except Exception:
        logger.exception('Fatal exception!')
    finally:
        sys.exit(return_code)


def heart_beat(_heartbeat_msg, _heartbeat_interval, state):
    if _heartbeat_interval:
        now = time.time()
        if (now - _heartbeat_msg) > _heartbeat_interval:
            logger.info(f"Bot heartbeat. PID={getpid()}, "
                        f"version='{__version__}', state='{state.name}'")
            _heartbeat_msg = now
    return _heartbeat_msg
