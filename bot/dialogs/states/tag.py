from aiogram.fsm.state import State, StatesGroup


class CreateTagState(StatesGroup):
    tag_name = State()
    tag_submit = State()


class TagState(StatesGroup):
    tags = State()
    create_tag = State()
    detail_tag = State()
    update_tag = State()
    confirm_update = State()
    delete_tag = State()
    confirm_delete = State()
