from functools import partial

from telebot import TeleBot, custom_filters

from bot import handlers as handlers
from bot import states as bot_states

# import tests.handlers as test_handlers


class Handler:
    def __init__(self, callback, **kwargs):
        self.callback = callback
        self.kwargs = kwargs


def get_start_handlers():
    return [
        Handler(callback=handlers.handle_start, commands=["start"]),
    ]


def get_registration_handlers():
    return [
        Handler(callback=handlers.handle_register, commands=["register"]),
        Handler(
            callback=handlers.handle_cancel_registration,
            commands=["cancel"],
            state=[
                bot_states.RegisterState.first_name,
                bot_states.RegisterState.last_name,
                bot_states.RegisterState.age,
            ],
        ),
        Handler(
            callback=handlers.handle_get_first_name,
            state=bot_states.RegisterState.first_name,
        ),
        Handler(
            callback=handlers.handle_get_last_name,
            state=bot_states.RegisterState.last_name,
        ),
        Handler(callback=handlers.handle_get_age, state=bot_states.RegisterState.age),
    ]


def get_show_data_handlers():
    return [
        Handler(callback=handlers.handle_show_data, commands=["show_data"]),
    ]


def get_delete_account_handlers():
    return [
        Handler(callback=handlers.handle_delete_account, commands=["delete_account"]),
        Handler(
            callback=handlers.handle_finish_delete_account,
            state=bot_states.DeleteAccountState.are_you_sure,
        ),
    ]


def create_bot(bot_token, pool):
    state_storage = bot_states.StateYDBStorage(pool)
    bot = TeleBot(bot_token, state_storage=state_storage)

    handlers = []
    handlers.extend(get_start_handlers())
    handlers.extend(get_registration_handlers())
    handlers.extend(get_show_data_handlers())
    handlers.extend(get_delete_account_handlers())

    for handler in handlers:
        bot.register_message_handler(
            partial(handler.callback, pool=pool), **handler.kwargs, pass_bot=True
        )

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    return bot
