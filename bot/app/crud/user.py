from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserCRUD:

    async def get_user_by_chat_id(
            self,
            chat_id: int,
            session: AsyncSession
    ) -> Optional[User]:
        user_db = await session.execute(
            select(User).where(User.chat_id == chat_id)
        )
        return user_db.scalars().first()

    async def create_user(
            self,
            user_in,
            session: AsyncSession
    ) -> User:
        user_in_data = user_in.dict()
        user_db = User(**user_in_data)
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)
        return user_db


user_crud = UserCRUD()
