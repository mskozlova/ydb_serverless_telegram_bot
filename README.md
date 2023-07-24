# How to set up a bot

## Creating Yandex Cloud function
Basic tutorial on telegram bot: https://cloud.yandex.com/en-ru/docs/functions/tutorials/telegram-bot-serverless

Create billing account & read about pricing https://cloud.yandex.com/en-ru/docs/functions/tutorials/telegram-bot-serverless#before-begin

1) Create a folder called for example telegram-bot-template (screenshots)
2) Create service account with roles (tutorial + screenshots)
4) Create API gateway https://cloud.yandex.com/en-ru/docs/functions/tutorials/telegram-bot-serverless#create-gateway
5) Create function with Python3.11 environment, make it public, create a first default version (screenshots)
6) Create a link between API gateway and function https://cloud.yandex.com/en-ru/docs/functions/tutorials/telegram-bot-serverless#function-bind-bot

## Creating a bot and linking it with the function
1) Create a telegram bot (screenshot)
2) Create a link between telegram bot and a function
curl \
  --request POST \
  --url https://api.telegram.org/bot<bot token>/setWebhook \
  --header 'content-type: application/json' \
  --data '{"url": "<API gateway domain>/fshtb-function"}'

At this stage command /start to your bot should lead to successful POST requests at API gateways (log screenshot) and successful function invocations (log screenshot). However function just wakes up and immidiately goes back to sleep again.

## Creating YDB database
1) Create a new YDB database resource
2) Go to navigation -> new SQL query -> Run
CREATE TABLE `user_personal_info`
(
    `user_id` Uint64,
    `last_name` Utf8,
    `first_name` Utf8,
    `age` Uint64,
    PRIMARY KEY (`user_id`)
);

CREATE TABLE `states`
(
    `user_id` Uint64,
    `state` Utf8,
    PRIMARY KEY (`user_id`)
);

We're going to create a database connection from code later.

## Make your bot do something
- Download the code from this repository.
- Edit create_function_version.sh - fill the IDs and tokens inside <>
- Execute create_function_version.sh to create a zip archive with the code and upload & create a new version of your function

Awesome! Now try your bot!

# Testing
