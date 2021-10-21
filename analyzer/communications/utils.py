import os

import yaml

from ..configuration.configuration import Config
from ..logger import Logger


def setup_telegram_constants(config: Config, logger: Logger, apprise_yml_path):
    enabled = True
    logger.info("Retrieving Telegram token and chat_id from apprise.yml file.")
    telegram_url = None
    if os.path.exists(apprise_yml_path):
        with open(apprise_yml_path) as f:
            try:
                parsed_urls = yaml.load(f, Loader=yaml.FullLoader)["urls"]
            except Exception:
                logger.error(
                    "Unable to correctly read apprise.yml file. Make sure it is correctly set up. Aborting."
                )
                enabled = False
            for url in parsed_urls:
                if url.startswith("tgram"):
                    telegram_url = url.split("//")[1]
        if not telegram_url:
            logger.error(
                "No telegram configuration was found in your apprise.yml file. Aborting."
            )
            enabled = False
    else:
        logger.error(
            f'Unable to find apprise.yml file at "{apprise_yml_path}". Aborting.'
        )
        enabled = False
    try:
        config.TELEGRAM_TOKEN = telegram_url.split("/")[0]
        config.TELEGRAM_CHAT_ID = telegram_url.split("/")[1]
        logger.info(
            f"Successfully retrieved Telegram configuration. "
            f"The bot will only respond to user in the chat with chat_id {config.TELEGRAM_CHAT_ID}"
        )
    except Exception:
        logger.error(
            "No chat_id has been set in the yaml configuration, anyone would be able to control your bot. Aborting."
        )
        enabled = False
    return enabled
