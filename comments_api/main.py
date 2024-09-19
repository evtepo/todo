import uvicorn
from fastapi import FastAPI

from api.v1.comment import router as comment_router
from config.settings import http_client, settings
from repository.cache import cache


async def lifespan(app: FastAPI):
    yield
    await cache.close()
    await http_client.aclose()


app = FastAPI(
    title=settings.title,
    lifespan=lifespan,
)

app.include_router(comment_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.localhost,
        port=settings.localport,
    )
