import os
import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from discord_websocket.ws import run_discord_websocket
from telegram_bot.dispatcher import run_telegram_consumer

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if TELEGRAM_TOKEN is None:
    print("[ERROR] Please add a telegram token inside .env file.")
    exit()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if DISCORD_TOKEN is None:
    print("[ERROR] Please add a discord token inside .env file.")
    exit()

MY_DISCORD_ID = os.getenv('MY_DISCORD_ID')
if MY_DISCORD_ID is None:
    print("[ERROR] Please add your discord ID inside .env file.")
    exit()

MY_TELEGRAM_CHAT_ID = os.getenv('MY_TELEGRAM_CHAT_ID')
if MY_TELEGRAM_CHAT_ID is None:
    print("[ERROR] Please add your telegram chat ID inside .env file.")
    exit()


async def main():
    shared_dict = {"status": "online", "lock": asyncio.Lock()}
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await asyncio.gather(
        run_telegram_consumer(bot, shared_dict),
        run_discord_websocket(bot, DISCORD_TOKEN, shared_dict, MY_DISCORD_ID, MY_TELEGRAM_CHAT_ID)
    )

if __name__ == "__main__":
    asyncio.run(main())
