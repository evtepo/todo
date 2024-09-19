from dotenv import load_dotenv
from httpx import AsyncClient
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    title: str = Field("Comments API", alias="PROJECT_NAME")
    localhost: str = Field("localhost", alias="LOCALHOST")
    localport: int = Field(8001, alias="LOCALPORT")

    pg_name: str = Field("comments_api", alias="POSTGRES_DB")
    pg_user: str = Field("postgres", alias="POSTGRES_USER")
    pg_password: str = Field("postgres", alias="POSTGRES_PASSWORD")
    pg_host: str = Field("localhost", alias="POSTGRES_HOST")
    pg_port: int = Field(5432, alias="POSTGRES_PORT")

    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    redis_port: str = Field("6379", alias="REDIS_PORT")

    todo_host: str = Field("todo_service", alias="TODO_HOST")
    todo_port: int = Field(80, alias="TODO_PORT")

    secret_key: str = Field("", alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGOROTHM")


settings = Settings()

cache_expire = 60

database_dsn = f"postgresql+asyncpg://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}:{settings.pg_port}/{settings.pg_name}"

todo_service_url = f"http://{settings.todo_host}:{settings.todo_port}/api/v1/auth/check-user-task/"

http_client: AsyncClient | None = AsyncClient()


async def get_client():
    return http_client
