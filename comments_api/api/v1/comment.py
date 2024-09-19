from typing import Annotated

from fastapi import APIRouter, Depends, Request, status, Query
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import get_client
from db.db_connect import get_session
from repository.cache import BaseCacheStorage, cache_storage
from repository.db import get_repository, BaseRepository
from services.comment import change_comment, del_comment, get_list_comments, new_comment
from schemas.comment import DeleteComment, CommentResponse, CreateComment, UpdateComment


router = APIRouter(prefix="/api/v1/comment", tags=["Comment"])

db_dependency = Annotated[AsyncSession, Depends(get_session)]
repository_dependency = Annotated[BaseRepository, Depends(get_repository)]
client_dependency = Annotated[AsyncClient, Depends(get_client)]
cache_dependency = Annotated[BaseCacheStorage, Depends(cache_storage)]


@router.get(
    "/",
    response_model=dict[str, dict | list[CommentResponse | None]],
    status_code=status.HTTP_200_OK,
)
async def get_comments(
    request: Request,
    session: db_dependency,
    repository: repository_dependency,
    cache: cache_dependency,
    task_id: str = Query(description="Task id"),
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=10, le=50, description="Page size"),
):
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse({"msg": "Authorization token is missing."}, status.HTTP_401_UNAUTHORIZED)

    headers = {"Authorization": token}

    return await get_list_comments(headers, task_id, page, size, session, repository, cache)


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    request: Request,
    comment_data: CreateComment,
    session: db_dependency,
    repository: repository_dependency,
    client: client_dependency,
    cache: cache_dependency,
):
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse({"msg": "Authorization token is missing."}, status.HTTP_401_UNAUTHORIZED)

    headers = {"Authorization": token}

    res = await new_comment(headers, comment_data, session, repository, client, cache)

    return res


@router.put("/", response_model=CommentResponse, status_code=status.HTTP_200_OK)
async def update_comment(
    request: Request,
    comment_data: UpdateComment,
    session: db_dependency,
    repository: repository_dependency,
    client: client_dependency,
    cache: cache_dependency,
):
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse({"msg": "Authorization token is missing."}, status.HTTP_401_UNAUTHORIZED)

    headers = {"Authorization": token}

    return await change_comment(headers, comment_data, session, repository, client, cache)


@router.delete("/", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_comment(
    request: Request,
    comment_data: DeleteComment,
    session: db_dependency,
    repository: repository_dependency,
    client: client_dependency,
    cache: cache_dependency,
):
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse({"msg": "Authorization token is missing."}, status.HTTP_401_UNAUTHORIZED)

    headers = {"Authorization": token}

    return await del_comment(headers, comment_data, session, repository, client, cache)
