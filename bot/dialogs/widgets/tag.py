import operator

from aiogram_dialog.widgets.kbd import Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format


def paginated_tags(on_click):
    return ScrollingGroup(
        Select(
            Format("{item.name}"),
            id="s_tag",
            item_id_getter=lambda item: f"{item.id}|{item.name}",
            items="tags",
            on_click=on_click,
        ),
        id="tag_ids",
        width=2,
        height=5,
    )
