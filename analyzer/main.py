#!python3
import logging
import sys
import time
from os import getpid
from typing import Any

from analyzer import __version__
from analyzer.analyzer import Analyzer
from analyzer.config.config import Config
from analyzer.enums import CommsMsgType, State
from analyzer.loggers import setup_logging, setup_logging_pre
from analyzer.misc import cleanup
from analyzer.utils.exceptions import AnalyzerException

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
            bot.processor.update_coin_list_data
        ).tag("updating coins")

        logger.info(f"Bot main state is: {bot.state}")
        _state = 0

        # While loop to keep going forever
        while bot.state != bot.state.EXIT:
            if bot.state == bot.state.RUNNING:
                _state = 0
                if _heartbeat_interval:
                    now = time.time()
                    if (now - _heartbeat_msg) > _heartbeat_interval:
                        logger.info(
                            f"Bot heartbeat. PID={getpid()}, "
                            f"version='{__version__}', state='{bot.state.name}'"
                        )
                        _heartbeat_msg = now
                bot.schedule.run_pending()
                time.sleep(config.BOT_SLEEP_TIME)
            elif bot.state == bot.state.RELOAD_CONFIG:
                logger.info("Reloading config...")
                config = load_config()
                bot.chatbot.send_msg(
                    {"type": CommsMsgType.STATUS, "status": "Reloaded config..."}
                )
                bot.state = State.RUNNING
            else:
                if _state == 0:
                    _state = 1
                    logger.warning("Bot has been stopped...")
                time.sleep(config.BOT_SLEEP_TIME)

    except SystemExit as e:  # pragma: no cover
        return_code = e
    except KeyboardInterrupt:
        logger.info("SIGINT received, aborting ...")
        return_code = 0
    except AnalyzerException as e:
        logger.error(str(e))
        return_code = 2
    except Exception:
        logger.exception("Fatal exception!")
    finally:
        cleanup(config)
        sys.exit(return_code)


def load_config() -> Config:
    config = Config()
    return config
