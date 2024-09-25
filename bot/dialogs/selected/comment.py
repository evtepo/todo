from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from dialogs.states.comment import CommentState

from configs.settings import comment_api_url
from db.cache import cache
from services.api import client_request


async def on_comments_selected(cq: CallbackQuery, widget: Any, manager: DialogManager):
    start_data = manager.current_context().dialog_data

    await manager.start(
        CommentState.task_comments,
        data={
            "task_id": start_data.get("id"),
            "task_name": start_data.get("name"),
        },
    )


async def on_comment_creation(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(CommentState.comment_name)


async def on_comment_name(cq: CallbackQuery, widget: Any, manager: DialogManager, comment: str):
    context_data = manager.current_context()
    context_data.dialog_data.update(commentary=comment)

    await manager.switch_to(CommentState.confirm_creation)


async def on_confirm_comment_creation(cq: CallbackQuery, widget: Any, manager: DialogManager):
    context_data = manager.current_context().dialog_data.copy()
    context_data.update(manager.start_data.copy())

    user = manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
        "json": context_data,
    }

    await client_request(f"{comment_api_url}", "POST", params=params)

    await manager.done()
