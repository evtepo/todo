from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from db.cache import cache
from dialogs.states.tag import TagState
from dialogs.states.task import TaskState
from dialogs.windows_setup import task_dialogs


router = Router(name=__name__)

router.include_routers(*task_dialogs)


@router.message(Command("task"))
async def get_tasks(message: Message, dialog_manager: DialogManager):
    if not await cache.get(message.from_user.full_name):
        await message.answer("Use /login to sign in to your account or /register to create.")
        return

    await dialog_manager.start(TaskState.tasks, mode=StartMode.RESET_STACK)


@router.message(Command("tags"))
async def get_tags(message: Message, dialog_manager: DialogManager):
    if not await cache.get(message.from_user.full_name):
        await message.answer("Use /login to sign in to your account or /register to create.")
        return

    await dialog_manager.start(TagState.tags, mode=StartMode.RESET_STACK)
