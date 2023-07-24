import json
import os
import random
import re

import telebot
from telebot import custom_filters

import bot.states as bot_states
import bot.handlers as handlers
from database.ydb_settings import pool
# import tests.handlers as test_handlers


state_storage = bot_states.StateYDBStorage(pool)
bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"), state_storage=state_storage)

##### handle welcome message
bot.register_message_handler(
    handlers.handle_start,
    commands=["start"],
    pass_bot=True
)

##### handle registration process
bot.register_message_handler(
    handlers.handle_register,
    commands=["register"],
    pass_bot=True
)
bot.register_message_handler(
    handlers.handle_cancel_registration,
    commands=["cancel"],
    state=[bot_states.RegisterState.first_name, bot_states.RegisterState.last_name, bot_states.RegisterState.age],
    pass_bot=True
)
bot.register_message_handler(
    handlers.handle_get_first_name,
    state=bot_states.RegisterState.first_name,
    pass_bot=True
)
bot.register_message_handler(
    handlers.handle_get_last_name,
    state=bot_states.RegisterState.last_name,
    pass_bot=True
)
bot.register_message_handler(
    handlers.handle_get_age,
    state=bot_states.RegisterState.age,
    pass_bot=True
)

##### show saved data
bot.register_message_handler(
    handlers.handle_show_data,
    commands=["show_data"],
    pass_bot=True
)

##### delete account
bot.register_message_handler(
    handlers.handle_delete_account,
    commands=["delete_account"],
    pass_bot=True
)
bot.register_message_handler(
    handlers.handle_finish_delete_account,
    state=bot_states.DeleteAccountState.are_you_sure,
    pass_bot=True
)

bot.add_custom_filter(custom_filters.StateFilter(bot))
