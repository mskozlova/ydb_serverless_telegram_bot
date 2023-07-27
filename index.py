import telebot

from logs import logger
from main import bot


def handler(event, _):
    logger.debug(f"New event: {event}")
    message = telebot.types.Update.de_json(event["body"])
    bot.process_new_updates([message])
    return {
        "statusCode": 200,
        "body": "!",
    }
