from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from configs.settings import task_api_url
from db.cache import cache
from dialogs.states.tag import CreateTagState, TagState
from services.api import client_request


async def on_chosen_tag(cq: CallbackQuery, widget: Any, manager: DialogManager, item_data: str):
    context = manager.current_context()
    tag_id, tag_name = item_data.split("|")
    context.dialog_data.update(id=tag_id, name=tag_name)

    await manager.switch_to(TagState.detail_tag)


async def on_change_tag_name(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(TagState.update_tag)


async def on_update_tag(cq: CallbackQuery, widget: Any, manager: DialogManager, new_name: str):
    context = manager.current_context()
    context.dialog_data.update(name=new_name)

    await manager.switch_to(TagState.confirm_update)


async def on_update_button(cq: CallbackQuery, widget: Any, manager: DialogManager):
    context_data = manager.current_context().dialog_data
    tag_id = context_data.get("id")

    user = manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
        "json": context_data
    }

    await client_request(f"{task_api_url}tag/{tag_id}", "PUT", params=params)

    await manager.switch_to(TagState.tags)


async def on_delete_tag(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(TagState.confirm_delete)


async def on_delete_button(cq: CallbackQuery, widget: Any, manager: DialogManager):
    context_data = manager.current_context().dialog_data
    tag_id = context_data.get("id")

    user = manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
    }

    await client_request(f"{task_api_url}tag/{tag_id}", "DELETE", params=params)

    await manager.switch_to(TagState.tags)


async def on_create_tag(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(CreateTagState.tag_name)


async def on_save_tag_name(cq: CallbackQuery, widget: Any, manager: DialogManager, tag_name: str):
    context = manager.current_context()
    context.dialog_data.update(name=tag_name)

    await manager.switch_to(CreateTagState.tag_submit)


async def on_tag_button_submit(cq: CallbackQuery, widget: Any, manager: DialogManager):
    context_data = manager.current_context().dialog_data

    user = manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
        "json": context_data,
    }

    await client_request(f"{task_api_url}tag/", "POST", params=params)

    await manager.start(TagState.tags, mode=StartMode.RESET_STACK)
