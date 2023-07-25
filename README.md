# About
This is a simple example of a telegram bot implementation. This code is designed to be run on [Yandex Cloud Serverless Function](https://cloud.yandex.com/en/docs/functions/quickstart/?from=int-console-help-center-or-nav) connected to [YDB database](https://cloud.yandex.com/en/docs/ydb/quickstart?from=int-console-help-center-or-nav) using [TeleBot (pyTelegramBotAPI)](https://pytba.readthedocs.io/en/latest/index.html) python3 package.

## Advantages

This repository can be used as a template for creating more complicated bots.

This implementation supports:
- full logging adapted to Yandex Cloud Functions
- handling user's states, which allows to conveniently process each text input in appropriate context and make complicated logics manageable
- handling a variety of Reply Keyboards and simple text inputs
- testing the bot (TBD)

## What does the bot do
List of bot's functions:
- asks for the user's first name, last name and age step-by-step
- checks correctness of the input data (age)
- saves the info into database (i.e. 'registers' the user)
- shows the info back when required
- supports deleting the database entry (i.e. 'deletes the account')

You can check out the instance of this bot [here](t.me/ydb_serverless_example_bot).

# How to set up an instance of the bot

## Creating Yandex Cloud function

1) Set up Yandex Cloud billing account - [instruction](https://cloud.yandex.com/en-ru/docs/functions/tutorials/telegram-bot-serverless#before-begin).
2) In Yandex Console create a folder for your resources. <details><summary>Screenshot</summary>
![Yandex Console Screenshot](screenshots/01-create-folder.png?raw=true "Title")</details>
3) Create a service account and assign it the `editor` and the `serverless.functions.invoker` roles for your folder. <details><summary>Screenshot</summary>
![Yandex Console Screenshot](screenshots/04-create-service-account.png?raw=true "Title")</details>
4) Create API gateway with the default specification. <details><summary>Screenshot</summary>
![Yandex Console Screenshot](screenshots/06-create-api-gateway.png?raw=true "Title")</details>
5) Create Serverless Function with Python3.11 environment. In the Overview tab make it public, in the Editor tab create a first default version. <details><summary>Screenshots</summary>
![Yandex Console Screenshot](screenshots/08-create-function.png?raw=true "Title") ![Yandex Console Screenshot](screenshots/08-make-function-public.png?raw=true "Title") ![Yandex Console Screenshot](screenshots/09-create-default-function-version.png?raw=true "Title")</details>
6) Copy your function ID. <details><summary>Screenshot</summary>
![Yandex Console Screenshot](screenshots/10-copy-fucntion-id.png?raw=true "Title")</details>
7) Create a link between API gateway and Function - edit API gateway specification and add the following code in the end, replacing `<function ID>` with copied value.
- ```
  /fshtb-function:
    post:
      x-yc-apigateway-integration:
        type: cloud_functions
        function_id: <function ID>
      operationId: fshtb-function
  ```

## Creating a bot and linking it with the function
1) Create a telegram bot sending `/newbot` command for BotFather in Telegram. <details><summary>Screenshot</summary>
![Yandex Console Screenshot](screenshots/05-create-telegram-bot.png?raw=true "Title")</details>
2) Create a link between telegram bot and a function. Run the following request from terminal, replacing `<YOUR BOT TOKEN>` with token from BotFather and `<API gateway domain>` with `Default domain` value from Overview tab of your API gateway.
```
curl \
  --request POST \
  --url https://api.telegram.org/bot<YOUR BOT TOKEN>/setWebhook \
  --header 'content-type: application/json' \
  --data '{"url": "<API gateway domain>/fshtb-function"}'
```

At this stage sending `/start` to your bot should lead to successful POST requests from API gateway and successful Function invocations, which you can track on their respective Logs tabs.
<details><summary>Successful API gateway logs</summary>

![Yandex Console Screenshot](screenshots/12-api-gateway-logs.png?raw=true "Title")
</details>
<details><summary>Successful function logs</summary>

![Yandex Console Screenshot](screenshots/13-function-logs.png?raw=true "Title")
</details>
</br>
Note: function does not do anything yet, except for waking up and going back to sleep.

## Creating YDB database
1) Create a new serverless YDB database resource in your folder.
2) Go to Navigation tab, click `New SQL query` and run the following request to create 2 necessary tables.
```
CREATE TABLE `user_personal_info`
(
    `user_id` Uint64,
    `last_name` Utf8,
    `first_name` Utf8,
    `age` Uint64,
    PRIMARY KEY (`user_id`)
);

COMMIT;

CREATE TABLE `states`
(
    `user_id` Uint64,
    `state` Utf8,
    PRIMARY KEY (`user_id`)
);
```

## Make your bot do something
1) Download the code from this repository.
2) Edit `create_function_version.sh` - fill the IDs and tokens inside `<>` brackets.
3) Execute `create_function_version.sh` to create a zip archive with the code and create a new version of your function using Yandex Cloud API.
4) (optional) Set commands for your bot via BotFather: send `/setcommands` anf the following text next <details><summary>Screenshot</summary>
![Yandex Console Screenshot](screenshots/15-set-bot-commands.png?raw=true "Title")</details>
```
start - show welcome message and bot description
register - store your name and age in the database
cancel - stop registering process
show_data - show your name and age stored in the database
delete_account - delete your info from the database
```

Awesome! Now try your bot!

# Testing
TBD...
