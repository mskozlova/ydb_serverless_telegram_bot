from telebot.handler_backends import State, StatesGroup
from telebot.storage.base_storage import StateContext, StateStorageBase

from database import model as db_model


# based on Telebot example
# https://github.com/eternnoir/pyTelegramBotAPI/blob/0f52ca688ffb7af6176d2f73fca92335dc3560eb/telebot/storage/redis_storage.py
class StateYDBStorage(StateStorageBase):
    """
    This class is for YDB storage to be used by the bot to track user states.
    """

    def __init__(self, ydb_pool):
        super().__init__()
        self.pool = ydb_pool

    def set_data(self, chat_id, user_id, key, value):
        """
        Set data for a user in a particular chat.
        """
        if db_model.get_state(self.pool, user_id) is None:
            return False

        full_state = db_model.get_state(self.pool, user_id)
        full_state["data"][key] = value

        db_model.set_state(self.pool, user_id, full_state)
        return True

    def get_data(self, chat_id, user_id):
        """
        Get data for a user in a particular chat.
        """
        full_state = db_model.get_state(self.pool, user_id)
        if full_state:
            return full_state.get("data", {})

        return {}

    def set_state(self, chat_id, user_id, state):
        if hasattr(state, "name"):
            state = state.name

        data = self.get_data(chat_id, user_id)
        full_state = {"state": state, "data": data}
        db_model.set_state(self.pool, user_id, full_state)
        return True

    def delete_state(self, chat_id, user_id):
        """
        Delete state for a particular user.
        """
        if db_model.get_state(self.pool, user_id) is None:
            return False

        db_model.clear_state(self.pool, user_id)
        return True

    def reset_data(self, chat_id, user_id):
        """
        Reset data for a particular user in a chat.
        """
        full_state = db_model.get_state(self.pool, user_id)
        if full_state:
            full_state["data"] = {}
            db_model.set_state(self.pool, user_id, full_state)
            return True
        return False

    def get_state(self, chat_id, user_id):
        states = db_model.get_state(self.pool, user_id)
        if states is None:
            return None
        return states.get("state")

    def get_interactive_data(self, chat_id, user_id):
        return StateContext(self, chat_id, user_id)

    def save(self, chat_id, user_id, data):
        full_state = db_model.get_state(self.pool, user_id)
        if full_state:
            full_state["data"] = data
            db_model.set_state(self.pool, user_id, full_state)
            return True


class RegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()


class DeleteAccountState(StatesGroup):
    are_you_sure = State()
