from aiogram_dialog import DialogManager

from configs.settings import comment_api_url
from db.cache import cache
from models.comment import Comment
from services.api import client_request


async def get_comments(dialog_manager: DialogManager, **kwargs):
    task_name = dialog_manager.start_data.get("task_name", "Unnamed task")
    task_id = dialog_manager.start_data.get("task_id", "")

    user = dialog_manager.event.from_user.full_name
    token = await cache.get(user)
    params = {
        "headers": {
            "Authorization": f"Bearer {token}",
        },
        "params": {
            "task_id": task_id,
            "page": 1,
            "size": 50,
        }
    }

    data, _ = await client_request(f"{comment_api_url}", "GET", params=params)

    comments = [Comment(**comment) for comment in data.get("data")]
    
    return {"comments": comments, "task_name": task_name, "task_id": task_id}