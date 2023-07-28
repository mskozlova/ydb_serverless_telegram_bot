from bot import keyboards, states
from database import model as db_model
from logs import logged_execution
from user_interaction import texts


@logged_execution
def handle_start(message, bot, pool):
    bot.send_message(message.chat.id, texts.START, reply_markup=keyboards.EMPTY)


@logged_execution
def handle_register(message, bot, pool):
    current_data = db_model.get_user_info(pool, message.from_user.id)

    if current_data:
        bot.send_message(
            message.chat.id,
            texts.ALREADY_REGISTERED.format(
                current_data["first_name"],
                current_data["last_name"],
                current_data["age"],
            ),
            reply_markup=keyboards.EMPTY,
        )
        return

    bot.send_message(
        message.chat.id,
        texts.FIRST_NAME,
        reply_markup=keyboards.get_reply_keyboard(["/cancel"]),
    )
    bot.set_state(
        message.from_user.id, states.RegisterState.first_name, message.chat.id
    )


@logged_execution
def handle_cancel_registration(message, bot, pool):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(
        message.chat.id,
        texts.CANCEL_REGISTER,
        reply_markup=keyboards.EMPTY,
    )


@logged_execution
def handle_get_first_name(message, bot, pool):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["first_name"] = message.text
    bot.set_state(message.from_user.id, states.RegisterState.last_name, message.chat.id)
    bot.send_message(
        message.chat.id,
        texts.LAST_NAME,
        reply_markup=keyboards.get_reply_keyboard(["/cancel"]),
    )


@logged_execution
def handle_get_last_name(message, bot, pool):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["last_name"] = message.text
    bot.set_state(message.from_user.id, states.RegisterState.age, message.chat.id)
    bot.send_message(
        message.chat.id,
        texts.AGE,
        reply_markup=keyboards.get_reply_keyboard(["/cancel"]),
    )


@logged_execution
def handle_get_age(message, bot, pool):
    if not message.text.isdigit():
        bot.send_message(
            message.chat.id,
            texts.AGE_IS_NOT_NUMBER,
            reply_markup=keyboards.EMPTY,
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
        texts.DATA_IS_SAVED.format(first_name, last_name, age),
        reply_markup=keyboards.EMPTY,
    )


@logged_execution
def handle_show_data(message, bot, pool):
    current_data = db_model.get_user_info(pool, message.from_user.id)

    if not current_data:
        bot.send_message(
            message.chat.id, texts.NOT_REGISTERED, reply_markup=keyboards.EMPTY
        )
        return

    bot.send_message(
        message.chat.id,
        texts.SHOW_DATA_WITH_PREFIX.format(
            current_data["first_name"], current_data["last_name"], current_data["age"]
        ),
        reply_markup=keyboards.EMPTY,
    )


@logged_execution
def handle_delete_account(message, bot, pool):
    current_data = db_model.get_user_info(pool, message.from_user.id)
    if not current_data:
        bot.send_message(
            message.chat.id, texts.NOT_REGISTERED, reply_markup=keyboards.EMPTY
        )
        return

    bot.send_message(
        message.chat.id,
        texts.DELETE_ACCOUNT,
        reply_markup=keyboards.get_reply_keyboard(texts.DELETE_ACCOUNT_OPTIONS),
    )
    bot.set_state(
        message.from_user.id, states.DeleteAccountState.are_you_sure, message.chat.id
    )


@logged_execution
def handle_finish_delete_account(message, bot, pool):
    bot.delete_state(message.from_user.id, message.chat.id)

    if message.text not in texts.DELETE_ACCOUNT_OPTIONS:
        bot.send_message(
            message.chat.id,
            texts.DELETE_ACCOUNT_UNKNOWN,
            reply_markup=keyboards.EMPTY,
        )
        return

    if texts.DELETE_ACCOUNT_OPTIONS[message.text]:
        db_model.delete_user_info(pool, message.from_user.id)
        bot.send_message(
            message.chat.id,
            texts.DELETE_ACCOUNT_DONE,
            reply_markup=keyboards.EMPTY,
        )
    else:
        bot.send_message(
            message.chat.id,
            texts.DELETE_ACCOUNT_CANCEL,
            reply_markup=keyboards.EMPTY,
        )
