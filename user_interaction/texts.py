START = (
    "Hello! This is a simple bot that can store your name and age, "
    "show them back to you and delete them if requested.\n\n"
    "List of commands:\n"
    "/start\n"
    "/register\n"
    "/show_data\n"
    "/delete_account"
)

FIRST_NAME = "Enter your first name."
LAST_NAME = "Enter your last name."
AGE = "Enter your age."
AGE_IS_NOT_NUMBER = "Age should be a positive number, try again."

SHOW_DATA = "First name: {}\nLast name: {}\nAge: {}"

DATA_IS_SAVED = "Your data is saved!\n" + SHOW_DATA
ALREADY_REGISTERED = "You are already registered!\n" + SHOW_DATA
SHOW_DATA_WITH_PREFIX = "Your data:\n" + SHOW_DATA

NOT_REGISTERED = "You are not registered yet, try /register."

CANCEL_REGISTER = "Cancelled! Your data is not saved."

DELETE_ACCOUNT = "Are you sure you want to delete your account?"
DELETE_ACCOUNT_OPTIONS = {"Yes!": True, "No..": False}
DELETE_ACCOUNT_UNKNOWN = "I don't understand this command."
DELETE_ACCOUNT_DONE = "Done! You can /register again."
DELETE_ACCOUNT_CANCEL = "Ok, stay for longer!"
