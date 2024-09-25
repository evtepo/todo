from aiogram.fsm.state import State, StatesGroup


class CreateTaskState(StatesGroup):
    task_name = State()
    task_description = State()
    task_status = State()
    task_tag = State()
    task_submit = State()


class TaskState(StatesGroup):
    tasks = State()
    create_task = State()
    detail_task = State()

    update_task = State()
    update_name = State()
    update_desc = State()
    update_status = State()
    update_tags = State()
    confirm_update = State()

    delete_task = State()
    confirm_delete = State()
