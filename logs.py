import logging
import traceback

from pythonjsonlogger import jsonlogger
from telebot.types import Message


# https://cloud.yandex.com/en/docs/functions/operations/function/logs-write#function-examples
class YcLoggingFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(YcLoggingFormatter, self).add_fields(log_record, record, message_dict)
        log_record["logger"] = record.name
        log_record["level"] = str.replace(
            str.replace(record.levelname, "WARNING", "WARN"), "CRITICAL", "FATAL"
        )


logHandler = logging.StreamHandler()
logHandler.setFormatter(YcLoggingFormatter("%(message)s %(level)s %(logger)s"))

logger = logging.getLogger("logger")
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)


def find_in_args(args, target_type):
    for arg in args:
        if isinstance(arg, target_type):
            return arg


def find_in_kwargs(kwargs, target_type):
    for kwarg in kwargs.values():
        if isinstance(kwarg, target_type):
            return kwarg


def get_message_info(*args, **kwargs):
    chat_id, text = "UNKNOWN", "UNKNOWN"

    if find_in_args(args, Message) is not None:
        message = find_in_args(args, Message)
        chat_id, text = message.chat.id, message.text
    elif find_in_kwargs(kwargs, Message) is not None:
        message = find_in_kwargs(args, Message)
        chat_id, text = message.chat.id, message.text

    return chat_id, text


def logged_execution(func):
    def wrapper(*args, **kwargs):
        chat_id, text = get_message_info(*args, **kwargs)

        logger.info(
            "[LOG] Starting {} - chat_id {}".format(func.__name__, chat_id),
            extra={
                "text": text,
                "arg": "{}".format(args),
                "kwarg": "{}".format(kwargs),
            },
        )
        try:
            func(*args, **kwargs)
            logger.info(
                "[LOG] Finished {} - chat_id {}".format(func.__name__, chat_id),
                extra={
                    "text": text,
                    "arg": "{}".format(args),
                    "kwarg": "{}".format(kwargs),
                },
            )
        except Exception as e:
            logger.error(
                "[LOG] Failed {} - chat_id {} - exception {}".format(
                    func.__name__, chat_id, e
                ),
                extra={
                    "text": text,
                    "arg": "{}".format(args),
                    "kwarg": "{}".format(kwargs),
                    "error": e,
                    "traceback": traceback.format_exc(),
                },
            )

    return wrapper
