from aiogram import Bot, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, CallbackQuery, Message
from aiogram_dialog import DialogManager


router = Router(name=__name__)


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(f"Hi, {message.from_user.full_name}")


async def set_commands(bot: Bot):
    commands = (
        BotCommand(command="register", description="Register an account"),
        BotCommand(command="login", description="Log into account"),
        BotCommand(command="tags", description="View tags"),
        BotCommand(command="task", description="View your tasks"),
    )
    await bot.set_my_commands(commands)
