import os

import telebot

from bot.structure import create_bot
from database.ydb_settings import get_ydb_pool
from logs import logger

YDB_ENDPOINT = os.getenv("YDB_ENDPOINT")
YDB_DATABASE = os.getenv("YDB_DATABASE")
BOT_TOKEN = os.getenv("BOT_TOKEN")


def handler(event, _):
    logger.debug(f"New event: {event}")

    pool = get_ydb_pool(YDB_ENDPOINT, YDB_DATABASE)
    bot = create_bot(BOT_TOKEN, pool)

    message = telebot.types.Update.de_json(event["body"])
    bot.process_new_updates([message])
    return {
        "statusCode": 200,
        "body": "!",
    }
