from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


async def on_cancel(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.done()