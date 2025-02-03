# TODO Service
Сервис предоставляет управлением задачами их категориями и комментариями через бота в Телеграм или админ панель.

## Запуск проекта
1. Перейти в корневую директорию проекта.
2. Выполнить команду:
   ```sh
   docker compose up --build

## Создание superuser'a:
1. Найти container id для todo_service
   ```sh
   docker ps
2. Ввести команду для входа в контейнер:
   ```sh
   docker exec -it <container id> bash
3. Создание superuser'a
   ```sh
   python manage.py creatsuperuser

## Task API
### Доступные эндоинты
#### Auth
url - `http://localhost:80/api/v1/auth/`
Регистрация - `POST` url + `register/`, body = {password: ...};   
Аутентификация - `POST` url + `login/`, body = {password: ...}.

#### Task
url - `http://localhost:80/api/v1/task/`
1. Создание задачи - `POST` url, body = {name: ..., description: ..., status: ..., tags: ...};    
2. Обновление задачи - `PUT` url + `task_id`, Опционально - body = {name: ..., description: ..., status: ..., tags: ...};   
3. Удаление задачи - `DELETE` url + `task_id`;   
4. Получение списка задач - `GET` url.   

#### Tag
url - `http://localhost:80/api/v1/tag/`
1. Создание тега - `POST` url, body = {name: ...};   
2. Обновление тега - `PUT` url + `tag_id`, Опционально - body = {name: ...};   
3. Удаление тега - `DELETE` url + `tag_id`;   
4. Получение списка тегов - `GET` url.

## Comment API
url - `http://localhost:81/api/v1/comment`
1. Создание комментария - `POST` url, body = {task_id: ..., commentary: ...};   
2. Обновление комментария - `PUT` url, body = {task_id: ...}, Опционально - {commentary: ...};   
3. Удаление комментария - `DELETE` url, body = {task_id: ...};   
4. Получение списка комментариев - `GET` url, params = task_id.

## Bot
Работа с сервисами происходит с помощью бота в телеграм - ```https://t.me/task_comment_bot```.
### Доступные команды:
1. ```/register``` - для регистрации аккаунта (Следующим сообщением ожидается пароль), в качестве логика в аккаунт вставляется имя пользователя в телеграм;
2. ```/login``` - для входа в аккаунт (Следующим сообщением ожидается пароль);
3. ```/tags``` - для получения списка тегов, их создания, обновления и удаления;
4. ```/task``` - для получения списка задач, их создания, обновления, удаления, добавления комментариев.

## Используемые технологии
| Компонент                       | Технология                               |
|---------------------------------|------------------------------------------|
| **Фреймворк для Task API**      | [Django](https://www.djangoproject.com/) |
| **Фреймворк для Comment API**   | [FastAPI](https://fastapi.tiangolo.com/) |
| **Веб-сервер**                  | [Nginx](https://www.nginx.com/)          |
| **База данных**                 | [MongoDB](https://www.mongodb.com/)      |
| **Кеширование**                 | [Redis](https://redis.io/)               |
| **Фреймворк для создания бота** | [aiogram](https://docs.aiogram.dev/)     |
| **Контейнеризация**             | [Docker](https://www.docker.com/)        |
