import logging
import asyncio
import json

import aiohttp
from aiogram import Bot

from discord_websocket.templates import get_open_msg, get_ping_msg


logger = logging.getLogger()


async def on_message(data: str, bot: Bot, my_discord_id: str, my_telegram_chat_id: str):
    try:
        msg = json.loads(data)
        author_name = msg['d']['author']['global_name']
        content = msg['d']['content']
        message_text = None

        if "t" in msg and msg["t"] == "MESSAGE_CREATE":
            if "guild_id" in msg["d"]:
                if my_discord_id in data:
                    message_text = f"🚨{author_name}: {content}"
                else:
                    if 'mention_roles' in msg['d']:
                        message_text = f"{author_name}: {content}"
            else:
                message_text = f"{author_name}: {content}."

            if message_text is not None:
                await bot.send_message(chat_id=my_telegram_chat_id, text=message_text)

    except Exception as exc:
        pass
        # logger.error(f"Error in processing message: {exc}", exc_info=True)


async def connect(uri: str, token: str, shared_dict: dict, bot: Bot, my_discord_id: str, my_telegram_chat_id):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(uri) as ws:
            open_msg = get_open_msg(token, shared_dict['status'])
            await ws.send_json(open_msg)

            async def read_messages():
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await on_message(msg.data, bot, my_discord_id, my_telegram_chat_id)
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        raise Exception("Connection closed")
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error("msg.type = aiohttp.WSMsgType.ERROR")
                        continue
                    await asyncio.sleep(0.1)

            async def send_ping():
                while True:
                    if shared_dict['status'] == 'idle':
                        raise Exception("AFK")
                    else:
                        ping_msg = get_ping_msg(shared_dict['status'],)
                    await ws.send_json(ping_msg)
                    await asyncio.sleep(15)

            await asyncio.gather(
                read_messages(),
                send_ping()
            )


async def run_discord_websocket(bot: Bot, token, shared_dict: dict, my_discord_id: str, my_telegram_chat_id):
    uri = "wss://gateway.discord.gg/?v=9&encoding=json"
    while True:
        try:
            await connect(uri, token, shared_dict, bot, my_discord_id, my_telegram_chat_id)
        except Exception as exc:
            while shared_dict['status'] == 'idle':
                await asyncio.sleep(5)
            logger.error(exc, exc_info=True)
            await asyncio.sleep(5)
