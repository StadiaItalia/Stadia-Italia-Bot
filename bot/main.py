from boilerplate.logger import Logger

import modules.configuration as configuration
from classes.database import BotDatabase
from classes.stadiaitaliabot import StadiaItaliaBot

logger = None
database = None

if configuration.logging_level:
    logger = Logger(level=configuration.logging_level)
else:
    raise Exception("Environment variable STADIA_ITALIA_LOGGING_LEVEL not found")

try:
    database = BotDatabase(host=configuration.host, user=configuration.user,
                           database=configuration.db_name, password=configuration.password,
                           configuration_repository=configuration.repository,
                           logger=logger)
except Exception as ex:
    raise Exception(f"Exception during database startup: {ex}")

StadiaItaliaBot.run_bot(database=database, logger=logger, token=configuration.token)
