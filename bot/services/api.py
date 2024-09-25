from httpx import AsyncClient, codes, Response


async def client_request(url: str, method: str, params: dict) -> dict:
    async with AsyncClient() as client:
        response: Response = await client.request(method, url, **params)
        if response.status_code in (codes.OK, codes.CREATED):
            return response.json(), response.status_code

        return {}, codes.BAD_REQUEST
