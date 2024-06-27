from aiogram.types import Message


async def command_start_handler(message: Message) -> None:
    await message.answer(f"Chat id = {message.chat.id}")


def set_discord_online(shared_dict: dict):
    async def callback(message: Message):
        async with shared_dict["lock"]:
            shared_dict["status"] = "online"
        print("STATUS IS ONLINE")
    return callback


def set_discord_offline(shared_dict: dict):
    async def callback(message: Message):
        async with shared_dict["lock"]:
            shared_dict["status"] = "idle"
        print("STATUS IS IDLE")
    return callback


async def message_handler(message: Message) -> None:
    try:
        await message.answer(text="Используйте команды /online /offline")
    except TypeError:
        await message.answer("Nice try!")
