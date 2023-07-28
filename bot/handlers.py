from telebot import TeleBot
from telebot.types import Message

from bot import keyboards, states
from database import model as db_model
from database.ydb_settings import pool
from logs import logged_execution
from user_interaction import texts


@logged_execution
def handle_start(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, texts.start_message, reply_markup=keyboards.empty)


@logged_execution
def handle_register(message: Message, bot: TeleBot):
    current_data = db_model.get_user_info(pool, message.from_user.id)

    if current_data:
        bot.send_message(
            message.chat.id,
            texts.already_registered_message.format(
                current_data["first_name"],
                current_data["last_name"],
                current_data["age"],
            ),
            reply_markup=keyboards.empty,
        )
        return

    bot.send_message(
        message.chat.id,
        texts.first_name_message,
        reply_markup=keyboards.get_reply_keyboard(["/cancel"]),
    )
    bot.set_state(
        message.from_user.id, states.RegisterState.first_name, message.chat.id
    )


@logged_execution
def handle_cancel_registration(message: Message, bot: TeleBot):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.chat.id,
        texts.cancelled_registration_message,
        reply_markup=keyboards.empty,
    )


@logged_execution
def handle_get_first_name(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["first_name"] = message.text
    bot.set_state(message.from_user.id, states.RegisterState.last_name, message.chat.id)
    bot.send_message(
        message.chat.id,
        texts.last_name_message,
        reply_markup=keyboards.get_reply_keyboard(["/cancel"]),
    )


@logged_execution
def handle_get_last_name(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["last_name"] = message.text
    bot.set_state(message.from_user.id, states.RegisterState.age, message.chat.id)
    bot.send_message(
        message.chat.id,
        texts.age_message,
        reply_markup=keyboards.get_reply_keyboard(["/cancel"]),
    )


@logged_execution
def handle_get_age(message: Message, bot: TeleBot):
    if not message.text.isdigit():
        bot.send_message(
            message.chat.id,
            texts.age_is_not_number_message,
            reply_markup=keyboards.empty,
        )
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        first_name = data["first_name"]
        last_name = data["last_name"]
        age = int(message.text)

    bot.delete_state(message.from_user.id, message.chat.id)
    db_model.add_user_info(pool, message.from_user.id, first_name, last_name, age)

    bot.send_message(
        message.chat.id,
        texts.data_saved_message.format(first_name, last_name, age),
        reply_markup=keyboards.empty,
    )


@logged_execution
def handle_show_data(message: Message, bot: TeleBot):
    current_data = db_model.get_user_info(pool, message.from_user.id)

    if not current_data:
        bot.send_message(
            message.chat.id, texts.not_registered_message, reply_markup=keyboards.empty
        )
        return

    bot.send_message(
        message.chat.id,
        texts.show_data_message.format(
            current_data["first_name"], current_data["last_name"], current_data["age"]
        ),
        reply_markup=keyboards.empty,
    )


@logged_execution
def handle_delete_account(message: Message, bot: TeleBot):
    current_data = db_model.get_user_info(pool, message.from_user.id)
    if not current_data:
        bot.send_message(
            message.chat.id, texts.not_registered_message, reply_markup=keyboards.empty
        )
        return

    bot.send_message(
        message.chat.id,
        texts.delete_account_message,
        reply_markup=keyboards.get_reply_keyboard(texts.delete_account_options),
    )
    bot.set_state(
        message.from_user.id, states.DeleteAccountState.are_you_sure, message.chat.id
    )


@logged_execution
def handle_finish_delete_account(message: Message, bot: TeleBot):
    bot.delete_state(message.from_user.id, message.chat.id)

    if message.text not in texts.delete_account_options:
        bot.send_message(
            message.chat.id,
            texts.delete_account_unknown_command,
            reply_markup=keyboards.empty,
        )
        return

    if texts.delete_account_options[message.text]:
        db_model.delete_user_info(pool, message.from_user.id)
        bot.send_message(
            message.chat.id,
            texts.delete_account_done_message,
            reply_markup=keyboards.empty,
        )
    else:
        bot.send_message(
            message.chat.id,
            texts.delete_account_cancelled_message,
            reply_markup=keyboards.empty,
        )
