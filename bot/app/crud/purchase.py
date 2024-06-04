from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.purchase import Purchase, Subscription


class PurchaseCRUD:

    async def get_purchase_by_number(
            self,
            purchase_number: str,
            session: AsyncSession
    ):
        purchase_db = await session.execute(
            select(Purchase).where(Purchase.number == purchase_number)
        )
        return purchase_db.scalars().first()

    async def create(
            self,
            purchase_in,
            session: AsyncSession
    ):
        data = purchase_in.dict()
        purchase = Purchase()
        purchase.from_dict(data)
        purchase.is_active = True
        session.add(purchase)
        await session.commit()
        await session.refresh(purchase)

        return purchase

    async def get_by_user(
            self,
            chat_id,
            session: AsyncSession
    ):
        purchases = await session.execute(
            select(Purchase).where(
                Purchase.subscribers.any(chat_id=chat_id)
            )
        )
        return purchases.scalars().all()

    async def add_subscriber(
            self,
            purchase_db,
            user_db,
            session: AsyncSession
    ):
        purchase_db.subscribers.append(user_db)
        session.add(purchase_db)
        await session.commit()
        await session.refresh(purchase_db)
        return purchase_db


purchase_crud = PurchaseCRUD()
