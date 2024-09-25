import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from configs.settings import bot_token
from handlers.auth import router as auth_router
from handlers.base import router as base_router, set_commands
from handlers.task import router as task_router


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def main():
    bot = Bot(bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_commands(bot)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(auth_router, base_router, task_router)
    setup_dialogs(dp)

    try:
        logging.info("The bot has started")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")

