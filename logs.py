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
    return find_in_args(kwargs.values(), target_type)


def get_message_info(*args, **kwargs):
    message_args = find_in_args(args, Message)
    if message_args is not None:
        return message_args.chat.id, message_args.text

    message_kwargs = find_in_kwargs(kwargs, Message)
    if message_kwargs is not None:
        return message_kwargs.chat.id, message_kwargs.text

    return "UNKNOWN", "UNKNOWN"


def logged_execution(func):
    def wrapper(*args, **kwargs):
        chat_id, text = get_message_info(*args, **kwargs)

        logger.info(
            f"[LOG] Starting {func.__name__} - chat_id {chat_id}",
            extra={
                "text": text,
                "arg": str(args),
                "kwarg": str(kwargs),
            },
        )
        try:
            func(*args, **kwargs)
            logger.info(
                f"[LOG] Finished {func.__name__} - chat_id {chat_id}",
                extra={
                    "text": text,
                    "arg": str(args),
                    "kwarg": str(kwargs),
                },
            )
        except Exception as e:
            logger.error(
                f"[LOG] Failed {func.__name__} - chat_id {chat_id} - exception {e}",
                extra={
                    "text": text,
                    "arg": str(args),
                    "kwarg": str(kwargs),
                    "error": e,
                    "traceback": traceback.format_exc(),
                },
            )

    return wrapper
