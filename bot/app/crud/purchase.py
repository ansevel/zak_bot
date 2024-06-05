from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.purchase import (Purchase, Preference, Restriction,
                                 Requirement)
from app.models.user import User


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
        session.add(purchase)
        await session.commit()
        await session.refresh(purchase)

        # This block to prevent MissingGreenlet (see https://sqlalche.me/e/14/xd2s)
        purchase_db = await session.execute(
            select(Purchase).options(joinedload(Purchase.subscribers)).where(
                Purchase.id == purchase.id
            )
        )
        return purchase_db.scalars().first()

    async def get_multi_by_user_id(  # Reform and delete
            self,
            chat_id,
            session: AsyncSession
    ):
        purchases = await session.execute(
            select(Purchase).join(Purchase.subscribers).where(
                User.chat_id == chat_id)
        )
        return purchases.unique().scalars().all()

    async def add_subscriber(
            self,
            purchase,
            user,
            session: AsyncSession
    ):
        purchase.subscribers.append(user)
        purchase.is_active = True
        session.add(purchase)
        await session.commit()
        await session.refresh(purchase)
        return purchase

    async def delete_subscription(
            self,
            purchase,
            user,
            session: AsyncSession
    ):
        purchase.subscribers.remove(user)
        if not purchase.subscribers:
            purchase.is_active = False
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


purchase_crud = PurchaseCRUD()
preference_crud = AddInfoCRUD(Preference)
requirement_crud = AddInfoCRUD(Requirement)
restriction_crud = AddInfoCRUD(Restriction)
