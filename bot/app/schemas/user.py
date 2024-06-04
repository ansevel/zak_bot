from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    chat_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    is_active: bool
    is_admin: bool


class UserRead(UserCreate):
    subscriptions: 'Optional[Purchase]' = None


from app.schemas.purchase import Purchase
UserRead.model_rebuild()
