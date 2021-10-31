#!python3
import time
import logging
import sys
from typing import Any
from os import getpid

# from analyzer import __version__
from analyzer import __version__
from .config.config import Config
from .utils.exceptions import AnalyzerException, OperationalException
from .loggers import setup_logging_pre, setup_logging
# from .utils import chat_helper
from .enums.state import State

from analyzer.analyzer import Analyzer

logger = logging.getLogger(__name__)


def main():
    """
    This function will initiate the bot and start the  loop.
    :return: None
    """

    return_code: Any = 1

    try:
        logger.info("Starting bot...")

        config = load_config()
        setup_logging_pre()
        setup_logging(config)

        bot = Analyzer(config)

        # Some constants to keep handy
        update_interval = config.UPDATE_COINS_INTERVAL
        _heartbeat_interval = config.HEARTBEAT_INTERVAL
        _heartbeat_msg = 0

        # Scheduling jobs
        bot.schedule.every(update_interval).seconds.do(
            bot.processor.update_coin_list_data).tag("updating coins")

        # While loop to keep going forever
        while bot.state != bot.state.EXIT:
            if bot.state == bot.state.RUNNING:
                if _heartbeat_interval:
                    now = time.time()
                    if (now - _heartbeat_msg) > _heartbeat_interval:
                        logger.info(f"Bot heartbeat. PID={getpid()}, "
                                    f"version='{__version__}', state='{bot.state.name}'")
                        _heartbeat_msg = now
                bot.schedule.run_pending()
                time.sleep(config.BOT_SLEEP_TIME)
            elif bot.state == bot.state.RELOAD_CONFIG:
                config = load_config()
            else:
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


def load_config() -> Config:
    config = Config()
    return config
