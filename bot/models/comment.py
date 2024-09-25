from dataclasses import dataclass
from datetime import datetime


@dataclass
class Comment:
    id: str
    commentary: str
    user_id: str
    task_id: str
    created_at: datetime
    updated_at: datetime
