import operator

from aiogram_dialog.widgets.kbd import Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format


def paginated_comment():
    return ScrollingGroup(
        Select(
            Format("{item.commentary}"),
            id="s_comment",
            item_id_getter=operator.attrgetter("id"),
            items="comments",
        ),
        id="comment_ids",
        width=2,
        height=5,
    )
