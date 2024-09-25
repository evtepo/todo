from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialogs.getters import (
    comment as comment_getter,
    tag as tag_getter,
    task as task_getter,
)
from dialogs.selected import (
    base,
    comment as comment_selected,
    task as task_selected,
)
from dialogs.states.comment import CommentState
from dialogs.states.task import CreateTaskState, TaskState
from dialogs.widgets.comment import paginated_comment
from dialogs.widgets.tag import paginated_tags
from dialogs.widgets.task import paginated_status, paginated_tasks
from dialogs.selected.comment import on_comments_selected


def tasks_window():
    return Window(
        Const("Tasks"),
        paginated_tasks(task_selected.on_chosen_task),
        Button(
            Const("Create a new task."),
            id="new_task",
            on_click=task_selected.on_create_task,
        ),
        Cancel(Const("Exit."), on_click=base.on_cancel),
        state=TaskState.tasks,
        getter=task_getter.tasks_window_getter,
    )


def detail_task():
    return Window(
        Format("Name: {name}"),
        Format("Description: {description}"),
        Format("Status: {status}"),
        Format("Tags {tags}"),
        Format("Date of creation: {created_at}"),
        Button(Const("Task comments"), id="task_comments", on_click=on_comments_selected),
        Button(Const("Change task"), id="change_task", on_click=task_selected.on_update_task),
        Button(Const("Delete task"), id="delete_task", on_click=task_selected.on_delete_task),
        Back(Const("Tasks")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TaskState.detail_task,
        getter=task_getter.get_task_info,
    )


def task_comments_window():
    return Window(
        Format("{task_name:.15} - comments"),
        paginated_comment(),
        Button(Const("Create comment"), id="comment_creation", on_click=comment_selected.on_comment_creation),
        Cancel(Const("Back to task info"), result={"switch_to_window": detail_task}),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=CommentState.task_comments,
        getter=comment_getter.get_comments,
    )


def comment_name():
    return Window(
        Const("Enter the commentary:"),
        TextInput(id="comment_name", on_success=comment_selected.on_comment_name),
        Back(Const("Back to task comments")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=CommentState.comment_name,
    )


def confirm_new_comment():
    return Window(
        Const("Confirm comment creation?"),
        Button(Const("Confirm"), id="confirm_new_comm", on_click=comment_selected.on_confirm_comment_creation),
        Back(Const("Change commentary")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=CommentState.confirm_creation,
    )


def new_task_name():
    return Window(
        Const("Enter the new task name or press 'Skip'"),
        TextInput(id="new_task_name", on_success=task_selected.on_new_task_name),
        Button(Const("Skip"), id="skip_name", on_click=task_selected.on_skip_name),
        Back(Const("Back to task details")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TaskState.update_name,
    )


def new_task_desc():
    return Window(
        Const("Enter the new task description or press 'Skip'"),
        TextInput(id="new_task_desc", on_success=task_selected.on_new_task_desc),
        Button(Const("Skip"), id="skip_desc", on_click=task_selected.on_skip_desc),
        Back(Const("Back to task name")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TaskState.update_desc,
    )


def new_task_status():
    return Window(
        Const("Select status or press 'Skip'"),
        paginated_status(task_selected.on_new_task_status),
        Button(Const("Skip"), id="skip_status", on_click=task_selected.on_skip_status),
        Back(Const("Back to task description")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TaskState.update_status,
        getter=task_getter.get_status_task,
    )


def new_task_tags():
    return Window(
        Const("Select tag or press 'Skip'"),
        paginated_tags(task_selected.on_new_task_tag),
        Button(Const("Skip"), id="skip_name", on_click=task_selected.on_skip_tags),
        Back(Const("Back to task status")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TaskState.update_tags,
        getter=tag_getter.get_tags,
    )


def confirm_task_update():
    return Window(
        Const("Confirm task updating?"),
        Button(Const("Confirm"), id="confirm_task_update", on_click=task_selected.on_confirm_update),
        Back(Const("Back to task tags")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TaskState.confirm_update,
    )


def confirm_task_delete():
    return Window(
        Const("Confirm task deletion?"),
        Button(Const("Confirm"), id="confirm_task_delete", on_click=task_selected.on_confirm_delete),
        Back(Const("Back to task details")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TaskState.confirm_delete,
    )


def create_task_name():
    return Window(
        Const("Enter the task name:"),
        TextInput(id="task_name", on_success=task_selected.on_save_task_name),
        Cancel(Const("Tasks"), result={"switch_to_window": tasks_window}),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=CreateTaskState.task_name,
    )


def create_task_description():
    return Window(
        Const("Enter the task description (Optional):"),
        Button(Const("Skip"), id="skip_button", on_click=task_selected.on_skip_click),
        TextInput(id="Task_desc", on_success=task_selected.on_save_task_desc),
        Back(Const("Change the task name")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=CreateTaskState.task_description,
    )


def create_task_status():
    return Window(
        Const("Select the task status:"),
        paginated_status(task_selected.on_chosen_status),
        Back(Const("Change the task description")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=CreateTaskState.task_status,
        getter=task_getter.get_status_task,
    )


def create_task_tag():
    return Window(
        Const("Select the task tag:"),
        paginated_tags(task_selected.on_chosen_tag),
        Back(Const("Change the task status")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=CreateTaskState.task_tag,
        getter=tag_getter.get_tags,
    )


def submit_new_task():
    return Window(
        Const("Confirm task creation"),
        Button(Const("Submit"), id="sumbit_button", on_click=task_selected.on_button_click),
        Back(Const("Change the task tag")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=CreateTaskState.task_submit,
    )
