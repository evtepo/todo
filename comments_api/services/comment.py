from fastapi import status
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import cache_expire
from models.comment import Comment
from repository.cache import BaseCacheStorage
from repository.db import BaseRepository
from schemas.comment import DeleteComment, CreateComment, UpdateComment
from services.check_user import check_user_n_task, get_user_id


async def get_list_comments(
    headers: dict,
    task_id: str,
    page: int,
    size: int,
    session: AsyncSession,
    repository: BaseRepository,
    cache: BaseCacheStorage,
):
    try:
        user_id = await get_user_id(headers)
    except Exception:
        return JSONResponse(
            {"msg": "Not authenticated or wrong task id."},
            status.HTTP_400_BAD_REQUEST,
        )

    filters = {"user_id": user_id, "task_id": task_id}

    prev_page = page - 1 if page - 1 > 0 else None
    next_page = page
    page = (page - 1) * size

    key = f"task:{task_id}:comments:page:size"
    data = await cache.get(key)
    data = []
    if not data:
        data = await repository.get(size, page, session, Comment, **filters)
        data_to_cache = [await comment.to_dict() for comment in data]

        await cache.set(key, data_to_cache, cache_expire)

    next_page = next_page + 1 if data and len(data) == size else None

    result = {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
        "data": data,
    }

    return result


async def new_comment(
    headers: dict,
    comment_data: CreateComment,
    session: AsyncSession,
    repository: BaseRepository,
    client: AsyncClient,
    cache: BaseCacheStorage,
):
    params = {"task_id": comment_data.task_id}
    if not await check_user_n_task(client, params, headers):
        return JSONResponse(
            {"msg": "Not authenticated or wrong task id."},
            status.HTTP_400_BAD_REQUEST,
        )

    user_id = await get_user_id(headers)
    temporary_data = comment_data.model_dump()
    temporary_data["user_id"] = user_id

    res = await repository.create(session, Comment, temporary_data)

    await cache.delete(f"task:{comment_data.task_id}:comments:*")

    return res


async def change_comment(
    headers: dict,
    comment_data: UpdateComment,
    session: AsyncSession,
    repository: BaseRepository,
    client: AsyncClient,
    cache: BaseCacheStorage,
):
    params = {"task_id": comment_data.task_id}
    if not await check_user_n_task(client, params, headers):
        return JSONResponse(
            {"msg": "Not authenticated or wrong task id."},
            status.HTTP_400_BAD_REQUEST,
        )

    user_id = await get_user_id(headers)

    filters = {"user_id": user_id, "task_id": comment_data.task_id, "id": comment_data.id}
    res = await repository.update(session, Comment, comment_data.model_dump(), **filters)

    await cache.delete(f"task:{comment_data.task_id}:comments:*")

    return res


async def del_comment(
    headers: dict,
    comment_data: DeleteComment,
    session: AsyncSession,
    repository: BaseRepository,
    client: AsyncClient,
    cache: BaseCacheStorage,
):
    params = {"task_id": comment_data.task_id}
    if not await check_user_n_task(client, params, headers):
        return JSONResponse(
            {"msg": "Not authenticated or wrong task id."},
            status.HTTP_400_BAD_REQUEST,
        )

    user_id = await get_user_id(headers)
    filters = {"id": comment_data.comment_id, "user_id": user_id, "task_id": comment_data.task_id}

    await repository.delete(session, Comment, **filters)

    await cache.delete(f"task:{comment_data.task_id}:comments:*")

    return {"msg": "Comment successfully deleted."}
