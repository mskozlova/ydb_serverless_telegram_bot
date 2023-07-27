start_message = (
    "Hello! This is a simple bot that can store your name and age, "
    "show them back to you and delete them if requested.\n\n"
    "List of commands:\n"
    "/start\n"
    "/register\n"
    "/show_data\n"
    "/delete_account"
)

cancel_message = "\n\nUse /cancel to abort the process."
first_name_message = "Enter your first name." + cancel_message
last_name_message = "Enter your last name." + cancel_message
age_message = "Enter your age." + cancel_message
age_is_not_number_message = "Age should be a number, try again." + cancel_message

data_format = (
    "First name: {}\n"
    "Last name: {}\n"
    "Age: {}"
)

data_saved_message = "Your data is saved!\n" + data_format
already_registered_message = "You are already registered!\n" + data_format
show_data_message = "Your data:\n" + data_format

not_registered_message = "You are not registered yet, try /register."

cancelled_registration_message = "Cancelled! Your data is not saved."

delete_account_message = "Are you sure you want to delete your account?"
delete_account_options = {
    "Yes!": True,
    "No..": False
}
delete_account_unknown_command = "I don't understand this command."
delete_account_done_message = "Done! You can /register again."
delete_account_cancelled_message = "Ok, stay for longer!"
