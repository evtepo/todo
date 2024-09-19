from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CommentMixin(BaseModel):
    task_id: str


class DeleteComment(CommentMixin):
    comment_id: UUID


class CreateComment(CommentMixin):
    commentary: str


class UpdateComment(CommentMixin):
    id: UUID
    commentary: str


class CommentResponse(CommentMixin):
    id: UUID
    user_id: str
    task_id: str
    commentary: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
