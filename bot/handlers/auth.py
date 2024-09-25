from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from httpx import codes

from configs.settings import cache_expire, task_api_url
from db.cache import cache
from dialogs.base_states import AuthState
from services.api import client_request


router = Router(name=__name__)


@router.message(Command("register"))
async def register_account(message: Message, state: FSMContext):
    await message.answer(
        """
        Enter your password:\nPassword must contain:
        - More than 8 characters;
        - Uppercase and lowercase letters;
        - Numbers;
        - Should not be similar to the username.
        """
    )

    await state.set_state(AuthState.waiting_for_password)
    await state.update_data(url=f"{task_api_url}auth/register/", method="POST")


@router.message(Command("login"))
async def login_into_account(message: Message, state: FSMContext):
    await message.answer("Enter your password:")

    await state.set_state(AuthState.waiting_for_password)
    await state.update_data(url=f"{task_api_url}auth/login/", method="POST")


@router.message(StateFilter(AuthState.waiting_for_password))
async def password_input(message: Message, state: FSMContext):
    password = message.text
    await message.delete()

    params = {
        "json": {
            "username": message.from_user.full_name,
            "password": password,
        },
    }
    state_data = await state.get_data()
    data, status = await client_request(state_data.get("url"), state_data.get("method"), params)
    if not data:
        await message.answer("Incorrect password.")

    if status == codes.OK:
        await cache.set(message.from_user.full_name, data.get("access"), cache_expire)
        await message.answer("Account login completed.")
    elif status == codes.CREATED:
        await message.answer("Account successfully registered")

    await state.clear()
