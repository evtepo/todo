from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StatusEnum(Enum):
    todo = "To do"
    in_progress = "In progress"
    review = "Review"
    completed = "Completed"
    canceled = "Canceled"


@dataclass
class Task:
    id: str
    name: str
    description: str
    status: str
    tags: list[str]
    users: list[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class Status:
    id: str
    name: str
