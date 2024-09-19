from django.contrib.auth.models import User
from django.db import models

from tasks.utils import generate_id


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date of creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date of update")

    class Meta:
        abstract = True


class Tag(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Tag name")

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.id = generate_id(f"{self.name}")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Task(DateMixin):
    class StatusChoices(models.TextChoices):
        todo = "To do"
        in_progress = "In progress"
        review = "Review"
        completed = "Completed"
        canceled = "Canceled"

    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Task name")
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.todo,
        max_length=20,
        verbose_name="Task status",
    )

    tags = models.ManyToManyField(Tag, related_name="tasks")
    users = models.ManyToManyField(User, related_name="tasks")

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.id = generate_id(f"{self.name}{self.status}")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
