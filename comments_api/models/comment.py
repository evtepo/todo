from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.db_connect import Base
from models.base import BaseMixin


class Comment(Base, BaseMixin):
    user_id: Mapped[str] = mapped_column(String(150), nullable=False)
    task_id: Mapped[str] = mapped_column(String(150), nullable=False)
    commentary: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        nullable=False,
        onupdate=datetime.now(),
    )

    async def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "task_id": self.task_id,
            "content": self.commentary,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
