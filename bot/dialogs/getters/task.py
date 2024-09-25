from aiogram_dialog import DialogManager

from configs.settings import task_api_url
from db.cache import cache
from models.task import Status, StatusEnum, Task
from services.api import client_request


async def tasks_window_getter(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
    }

    data, _ = await client_request(f"{task_api_url}task/", "GET", params=params)
    tasks = [Task(**task) for task in data]

    return {"tasks": tasks}


async def get_status_task(dialog_manager: DialogManager, **kwargs):
    status = (
        Status(id=f"{status.value}_id", name=status.value) for status in StatusEnum
    )
    return {"status": status}


async def get_task_info(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.event.from_user.full_name
    token = await cache.get(user)

    dialog_data = dialog_manager.current_context().dialog_data
    id, name = dialog_data.get("id"), dialog_data.get("name")

    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
    }

    data, _ = await client_request(f"{task_api_url}task/{id}", "GET", params=params)
    description = data.get("description")
    status = data.get("status")
    tags = data.get("tags")

    dialog_data.update(
        description=description,
        status=status,
        tags=tags,
    )

    window_tags = [tag.get("name") for tag in tags]

    return {
        "name": name,
        "description": description,
        "status": status,
        "tags": window_tags,
        "created_at": data.get("created_at"),
    }
