from aiogram.fsm.state import State, StatesGroup


class CommentState(StatesGroup):
    task_comments = State()
    comment_name = State()
    confirm_creation = State()
