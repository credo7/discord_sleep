from functools import partial

from aiogram import Dispatcher, Bot

from aiogram.filters import CommandStart, Command

from telegram_bot.handlers import (
    command_start_handler,
    message_handler,
    set_discord_offline,
    set_discord_online
)


def get_dispatcher(shared_dict: dict) -> Dispatcher:
    dp = Dispatcher()

    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(set_discord_online(shared_dict), Command('online'))
    dp.message.register(set_discord_offline(shared_dict), Command('offline'))
    dp.message.register(message_handler)

    return dp


async def run_telegram_consumer(bot: Bot, shared_dict: dict):
    dp = get_dispatcher(shared_dict)
    await dp.start_polling(bot)
