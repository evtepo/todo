import os


bot_token = os.environ.get("TOKEN", "")

comment_api_url = os.environ.get("COMMENTS_API_URL", "http://nginx_comments:81/api/v1/comments/")
task_api_url = os.environ.get("TASK_API_URL", "http://nginx_todo:80/api/v1/")

redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")

redis_url = f"redis://{redis_host}:{redis_port}"
cache_expire = 900
