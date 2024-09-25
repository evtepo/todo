from aiogram_dialog import Dialog

from dialogs.windows import tag, task


task_dialogs = [
    # Task data (rud)
    Dialog(
        task.tasks_window(),
        task.detail_task(),
        task.new_task_name(),
        task.new_task_desc(),
        task.new_task_status(),
        task.new_task_tags(),
        task.confirm_task_update(),
        task.confirm_task_delete(),
    ),
    # Comments data (rud)
    Dialog(
        task.task_comments_window(),
        task.comment_name(),
        task.confirm_new_comment(),
    ),
    # Task creation
    Dialog(
        task.create_task_name(),
        task.create_task_description(),
        task.create_task_status(),
        task.create_task_tag(),
        task.submit_new_task(),
    ),
    # Tag data (rud)
    Dialog(
        tag.tags_window(),
        tag.tag_detail(),
        tag.update_tag(),
        tag.submit_tag_update(),
        tag.submit_tag_delete(),
    ),
    # Tag creation
    Dialog(
        tag.new_tag_window(),
        tag.submit_new_tag(),
    )
]
