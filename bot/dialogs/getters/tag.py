from aiogram_dialog import DialogManager

from configs.settings import task_api_url
from db.cache import cache
from models.tag import Tag
from services.api import client_request


async def get_tags(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
    }

    data, _ = await client_request(f"{task_api_url}tag/", "GET", params=params)
    tags = [Tag(**tag) for tag in data]

    return {"tags": tags}


async def get_detail_data(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.current_context().dialog_data
    tag_id = dialog_data.get("id")
    tag_name = dialog_data.get("name")

    return {"id": tag_id, "name": tag_name}
