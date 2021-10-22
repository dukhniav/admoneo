import os
import yaml

from typing import Dict, Any

from ..configuration.configuration import Config
from ..logger import Logger


def setup_telegram_constants(config: Config, logger: Logger):
    enabled = True
    logger.info("Retrieving Telegram token and chat_id from apprise.yml file.")
    token = config.TGRAM_TOKEN
    chat_id = config.TGRAM_CHAT_ID

    if token == None or chat_id == None:
        enabled = False
        logger.error(
            "Unable to extract telegram secrets. Make sure it's correctly set-up. Aborting...")

    config.TGRAM_ENABLED = enabled
    return enabled


def facts_to_str(self, user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])
