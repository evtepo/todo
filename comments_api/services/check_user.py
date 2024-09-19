import jwt
from fastapi import status
from httpx import AsyncClient, Response

from config.settings import settings, todo_service_url


async def check_user_n_task(client: AsyncClient, params: dict, headers: dict = {}):
    response: Response = await client.get(todo_service_url, headers=headers, params=params)
    if response.status_code == status.HTTP_200_OK:
        return True

    return False


async def get_user_id(headers: dict):
    token = headers.get("Authorization").split()[1]
    user_id = str(jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm]).get("user_id"))

    return user_id
