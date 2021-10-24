import os
import yaml

from typing import Dict, Any

from ..config import Config
from ..logger import Logger
from ..utils import exceptions


def setup_telegram_constants(config: Config, logger: Logger):
    config.TGRAM_ENABLED = True
    logger.info("Retrieving Telegram token and chat_id from credentials.cfg file")
    try:
        token = config.TGRAM_TOKEN
        chat_id = config.TGRAM_CHAT_ID
    except exceptions.TelegramException as e:
        config.TGRAM_ENABLED = False
        print(e)

    if token == None or chat_id == None:
        config.TGRAM_ENABLED = False
        logger.error(
            "Unable to extract telegram secrets. Make sure it's correctly set-up. Aborting...")

def facts_to_str(self, user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])
