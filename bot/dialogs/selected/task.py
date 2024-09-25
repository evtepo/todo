from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from configs.settings import task_api_url
from db.cache import cache
from dialogs.states.task import CreateTaskState, TaskState
from services.api import client_request


async def on_chosen_task(cq: CallbackQuery, widget: Any, manager: DialogManager, item_data: str):
    id, name = item_data.split("|")
    context = manager.current_context()
    context.dialog_data.update(
        id=id,
        name=name,
    )

    await manager.switch_to(TaskState.detail_task)


async def on_update_task(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(TaskState.update_name)


async def on_new_task_name(cq: CallbackQuery, widget: Any, manager: DialogManager, name: str):
    context = manager.current_context()
    context.dialog_data.update(name=name)

    await manager.switch_to(TaskState.update_desc)


async def on_skip_name(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(TaskState.update_desc)


async def on_new_task_desc(cq: CallbackQuery, widget: Any, manager: DialogManager, desc: str):
    context = manager.current_context()
    context.dialog_data.update(description=desc)

    await manager.switch_to(TaskState.update_status)


async def on_skip_desc(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(TaskState.update_status)


async def on_new_task_status(cq: CallbackQuery, widget: Any, manager: DialogManager, status: str):
    context = manager.current_context()
    context.dialog_data.update(status=status)

    await manager.switch_to(TaskState.update_tags)


async def on_skip_status(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(TaskState.update_tags)


async def on_new_task_tag(cq: CallbackQuery, widget: Any, manager: DialogManager, tag: str):
    context = manager.current_context()
    tags = []
    new_tag = tag.split("|")[0]
    for tag in context.dialog_data.get("tags"):
        tags.append(tag.get("id"))

    tags.append(new_tag)
    context.dialog_data.update(tags=tags)

    await manager.switch_to(TaskState.confirm_update)


async def on_skip_tags(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(TaskState.confirm_update)


async def on_confirm_update(cq: CallbackQuery, widget: Any, manager: DialogManager):
    context = manager.current_context()

    user = manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
        "json": context.dialog_data,
    }
    print(params)
    task_id = context.dialog_data.get("id")

    await client_request(f"{task_api_url}task/{task_id}", "PUT", params=params)

    await manager.switch_to(TaskState.tasks)


async def on_delete_task(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(TaskState.confirm_delete)


async def on_confirm_delete(cq: CallbackQuery, widget: Any, manager: DialogManager):
    context = manager.current_context()

    user = manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
    }

    task_id = context.dialog_data.get("id")
    _, _ = await client_request(f"{task_api_url}task/{task_id}", "DELETE", params=params)
    
    await manager.done()


async def on_create_task(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.start(CreateTaskState.task_name)


async def on_save_task_name(cq: CallbackQuery, widget: Any, manager: DialogManager, task_name: str):
    context = manager.current_context()
    context.dialog_data.update(name=task_name)

    await manager.switch_to(CreateTaskState.task_description)


async def on_skip_click(cq: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.switch_to(CreateTaskState.task_status)


async def on_save_task_desc(cq: CallbackQuery, widget: Any, manager: DialogManager, task_desc: str):
    context = manager.current_context()
    context.dialog_data.update(description=task_desc)

    await manager.switch_to(CreateTaskState.task_status)


async def on_chosen_status(cq: CallbackQuery, widget: Any, manager: DialogManager, task_status: str):
    context = manager.current_context()
    context.dialog_data.update(status=task_status)

    await manager.switch_to(CreateTaskState.task_tag)


async def on_chosen_tag(cq: CallbackQuery, widget: Any, manager: DialogManager, tag_id: str):
    context = manager.current_context()
    tag_id = tag_id.split("|")[0]
    context.dialog_data.update(tags=[tag_id])

    await manager.switch_to(CreateTaskState.task_submit)


async def on_button_click(cq: CallbackQuery, widget: Any, manager: DialogManager):
    context = manager.current_context()

    user = manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
        "json": context.dialog_data
    }

    print(params)

    _, _ = await client_request(f"{task_api_url}task/", "POST", params=params)

    await manager.start(TaskState.tasks)
