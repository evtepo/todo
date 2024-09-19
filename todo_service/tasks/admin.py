from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from tasks.models import Tag, Task


class AdminMixin(admin.ModelAdmin):
    show_full_result_count = False

    class Meta:
        abstract = True


@admin.register(Tag)
class TagAdmin(AdminMixin):
    exclude = ("id",)
    list_display = ("name",)


@admin.register(Task)
class TaskAdmin(AdminMixin):
    exclude = ("id",)
    list_display = (
        "name",
        "description",
        "status",
        "list_tags",
        "list_users",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "tags", "users")
    list_editable = ("status",)
    search_fields = ("name",)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related("tags", "users")

    def list_tags(self, obj: Task) -> str:
        return ", ".join(tag.name for tag in obj.tags.all())

    def list_users(self, obj: Task) -> str:
        return ", ".join(user.username for user in obj.users.all())

    list_tags.short_description = "Tags"
    list_users.short_description = "Users"
