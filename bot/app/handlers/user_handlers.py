from math import ceil

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app.constants.common import MAX_LENGTH_MESSAGE
from app.constants.info_messages import (EMPTY_LIST, HELP_MESSAGE,
                                         START_MESSAGE, SUBSCRIPTION_ADDED,
                                         SUBSCRIPTION_DELETED)
from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.crud.purchase import purchase_crud
from app.crud.relations import subscription_crud
from app.crud.user import user_crud
from app.keyboards.purchase import (add_subscription_button,
                                    delete_subscription_button,
                                    get_inline_button)
from app.schemas.user import UserCreate
from app.services.parser import get_purchase_from_web

router = Router()


@router.message(CommandStart())
async def command_start_process(message: Message):
    user = UserCreate(
        chat_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        is_active=True,
        is_admin=(
            True if message.from_user.id in settings.admin_ids else False)
    )
    async with AsyncSessionLocal() as session:
        if await user_crud.get_user_by_chat_id(user.chat_id, session) is None:
            await user_crud.create_user(user, session)
    await message.answer(text=START_MESSAGE)


@router.message(Command(commands='help'))
async def command_help_process(message: Message):
    await message.answer(text=HELP_MESSAGE)


@router.message(Command(commands='list'))
async def command_list_process(message: Message):
    async with AsyncSessionLocal() as session:
        purchases = await purchase_crud.get_by_user(
            message.from_user.id, session)
    await message.answer(text=EMPTY_LIST)


@router.message(F.text.isdigit())
async def find_purchase(message: Message):
    purchase_obj = await get_purchase_from_web(message.text)
    formatted_data = purchase_obj.common_data_message_text()
    formatted_data = purchase_obj.add_long_additional_info(formatted_data)
    # if purchase_data.get('errors') is not None:  # raise exception > errors handler
    #     await message.answer(text=formatted_data)
    length = len(formatted_data)
    if length > MAX_LENGTH_MESSAGE:
        offset = 0
        message_count = ceil(length / MAX_LENGTH_MESSAGE)
        for _ in range(message_count - 1):
            await message.answer(
                text=formatted_data[offset:MAX_LENGTH_MESSAGE + offset])
            offset += MAX_LENGTH_MESSAGE
        await message.answer(text=formatted_data[offset:],
                             reply_markup=get_inline_button(message))
    else:
        await message.answer(text=formatted_data,
                             reply_markup=get_inline_button(message))


@router.callback_query(F.data == 'add_subscription')
async def add_subscription(callback: CallbackQuery):
    num = '0142200001324013160'
    async with AsyncSessionLocal() as session:
        purchase_obj = await get_purchase_from_web(num)
        purchase_db = await purchase_crud.get_purchase_by_number(num, session)
        if purchase_db is None:
            purchase_db = await purchase_crud.create(
                purchase_obj, session)
        user_db = await user_crud.get_user_by_chat_id(
            callback.from_user.id, session)
        await purchase_crud.add_subscriber(purchase_db, user_db, session)
    await callback.message.edit_reply_markup(
        reply_markup=delete_subscription_button
    )
    await callback.answer(text=SUBSCRIPTION_ADDED)


@router.callback_query(F.data == 'delete_subscription')
async def delete_subscritpion(callback: CallbackQuery):
    # delete subscription
    await callback.message.edit_reply_markup(
        reply_markup=add_subscription_button
    )
    await callback.answer(text=SUBSCRIPTION_DELETED)
