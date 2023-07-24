import os

from pyrogram import Client
import pytest


api_id = os.environ.get("TELEGRAM_API_ID")
api_hash = os.environ.get("TELEGRAM_API_HASH")
client_name = "languagecardsbottester"
workdir = "/Users/mariakozlova/ml_and_staff/language_cards_bot/tests"


@pytest.fixture
def test_client():
    client = Client(client_name, api_id, api_hash, workdir=workdir)
    client.start()
    yield client
    client.stop()


@pytest.fixture
def chat_id():
    return "@language_cards_tester_bot"
