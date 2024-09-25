import operator

from aiogram_dialog.widgets.kbd import Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format


def paginated_tasks(on_click):
    return ScrollingGroup(
        Select(
            Format("{item.name}"),
            id="s_tasks",
            item_id_getter=lambda item: f"{item.id}|{item.name}",
            items="tasks",
            on_click=on_click,
        ),
        id="task_ids",
        width=2,
        height=5,
    )


def paginated_status(on_click):
    return ScrollingGroup(
        Select(
            Format("{item.name}"),
            id="s_status",
            item_id_getter=operator.attrgetter("name"),
            items="status",
            on_click=on_click,
        ),
        id="status_ids",
        width=2,
        height=5,
    )
