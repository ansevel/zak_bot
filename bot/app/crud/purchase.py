from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.purchase import (Purchase, Preference, Restriction,
                                 Requirement)


class AddInfoCRUD:

    def __init__(self, model):
        self.model = model

    async def create(
            self,
            data_in,
            session: AsyncSession,
    ):
        item = self.model(long_description=data_in.long_description)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    async def get_by_long_description(
            self,
            data_in,
            session: AsyncSession,
    ):
        item = await session.execute(
            select(self.model).where(
                self.model.long_description == data_in.long_description
            )
        )
        return item.scalars().first()

    async def get_or_create(
            self,
            data_in,
            session: AsyncSession
    ):
        item = await self.get_by_long_description(data_in, session)
        if item is None:
            item = await self.create(data_in, session)
        return item


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
            purchase,
            user,
            session: AsyncSession
    ):
        purchase.subscribers.append(user)
        session.add(purchase)
        await session.commit()
        await session.refresh(purchase)
        return purchase

    async def append_add_info(
            self,
            purchase,
            preferences,
            requirements,
            restrictions,
            session: AsyncSession
    ):
        if preferences:
            purchase.preferences.extend(preferences)
        if requirements:
            purchase.requirements.extend(requirements)
        if restrictions:
            purchase.restrictions.extend(restrictions)
        session.add(purchase)
        await session.commit()
        await session.refresh(purchase)
        return purchase


purchase_crud = PurchaseCRUD()
preference_crud = AddInfoCRUD(Preference)
requirement_crud = AddInfoCRUD(Requirement)
restriction_crud = AddInfoCRUD(Restriction)
