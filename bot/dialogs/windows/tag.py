from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

from dialogs.getters import tag as tag_getters
from dialogs.selected import base, tag as tag_selected
from dialogs.widgets.tag import paginated_tags
from dialogs.states.tag import CreateTagState, TagState


def tags_window():
    return Window(
        Const("Tags"),
        paginated_tags(tag_selected.on_chosen_tag),
        Button(Const("Create a new tag"), id="new_tag", on_click=tag_selected.on_create_tag),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TagState.tags,
        getter=tag_getters.get_tags,
    )


def tag_detail():
    return Window(
        Format("{name}"),
        Button(Const("Change the tag name"), id="change_tag_name", on_click=tag_selected.on_change_tag_name),
        Button(Const("Delete tag"), id="delete_tag", on_click=tag_selected.on_delete_tag),
        Back(Const("Tags")),
        state=TagState.detail_tag,
        getter=tag_getters.get_detail_data,
    )


def update_tag():
    return Window(
        Const("Enter the new tag name:"),
        TextInput(id="new_tag_name", on_success=tag_selected.on_update_tag),
        Back(Const("Back")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TagState.update_tag,
    )


def submit_tag_update():
    return Window(
        Const("Confirm tag updating"),
        Button(Const("Confirm"), id="confirm_tag_update", on_click=tag_selected.on_update_button),
        Back(Const("Change tag name")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TagState.confirm_update,
    )


def submit_tag_delete():
    return Window(
        Const("Confirm tag deletion"),
        Button(Const("Confirm"), id="confrim_tag_delete", on_click=tag_selected.on_delete_button),
        Back(Const("Back")),
        Cancel(Const("Exit"), on_click=base.on_cancel),
        state=TagState.confirm_delete,
    )


def new_tag_window():
    return Window(
        Const("Enter the tag name:"),
        TextInput(id="tag_input", on_success=tag_selected.on_save_tag_name),
        Cancel(Const("Exit"), result={"switch_to_window": tags_window}),
        state=CreateTagState.tag_name,
    )


def submit_new_tag():
    return Window(
        Const("Confirm tag creation"),
        Button(Const("Submit"), id="submit_tag_button", on_click=tag_selected.on_tag_button_submit),
        Back(Const("Change the tag name")),
        Cancel(Const("Exit"), result={"switch_to_window": tags_window}),
        state=CreateTagState.tag_submit,
    )
