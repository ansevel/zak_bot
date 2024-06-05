from math import ceil

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app.constants.common import MAX_LENGTH_MESSAGE
from app.constants.info_messages import (EMPTY_LIST, HELP_MESSAGE,
                                         START_MESSAGE, SUBSCRIPTION_ADDED,
                                         SUBSCRIPTION_DELETED, LIST)
from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.crud.purchase import (preference_crud, purchase_crud,
                               restriction_crud, requirement_crud)
from app.crud.user import user_crud
from app.keyboards.purchase import (add_subscription_button,
                                    delete_subscription_button,
                                    get_inline_button)
from app.schemas.purchase import Purchase
from app.schemas.user import UserCreate
from app.services.utils import (get_purchase_num_form_message,
                                get_purchse_num_from_user)
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
        subscriptions_db = await purchase_crud.get_multi_by_user_id(
            message.from_user.id, session)
    if subscriptions_db:
        await message.answer(text=LIST)
        for subscription in subscriptions_db:
            purchase_obj = Purchase.model_validate(subscription)
            formatted_data = purchase_obj.common_data_message_text()
            formatted_data = purchase_obj.add_long_additional_info(
                formatted_data)
            length = len(formatted_data)
            if length > MAX_LENGTH_MESSAGE:
                offset = 0
                message_count = ceil(length / MAX_LENGTH_MESSAGE)
                for _ in range(message_count - 1):
                    await message.answer(
                        text=formatted_data[offset:MAX_LENGTH_MESSAGE + offset]
                    )
                    offset += MAX_LENGTH_MESSAGE
                await message.answer(text=formatted_data[offset:],
                                     reply_markup=delete_subscription_button)
            else:
                await message.answer(text=formatted_data,
                                     reply_markup=delete_subscription_button)
    else:
        await message.answer(text=EMPTY_LIST)


# @router.message(F.text.isdigit())
@router.message()
async def find_purchase(message: Message):
    number = get_purchse_num_from_user(message.text)
    if number is None:
        await message.answer(text='Здусь будет ошибка введенных данных')
    purchase_obj = await get_purchase_from_web(number)
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
                             reply_markup=await get_inline_button(number))
    else:
        await message.answer(text=formatted_data,
                             reply_markup=await get_inline_button(number))


@router.callback_query(F.data == 'add_subscription')
async def add_subscription(callback: CallbackQuery):
    num = get_purchase_num_form_message(callback.message.text)
    async with AsyncSessionLocal() as session:
        purchase_obj = await get_purchase_from_web(num)
        purchase_db = await purchase_crud.get_purchase_by_number(num, session)
        if purchase_db is None:
            purchase_db = await purchase_crud.create(
                purchase_obj, session)
        user_db = await user_crud.get_user_by_chat_id(
            callback.from_user.id, session)

        await purchase_crud.add_subscriber(purchase_db, user_db, session)

        preferences = []
        if purchase_obj.preferences is not None:
            for p in purchase_obj.preferences:
                preferences.append(
                    await preference_crud.get_or_create(p, session)
                )

        restrictions = []
        if purchase_obj.restrictions is not None:
            for r in purchase_obj.restrictions:
                restrictions.append(
                    await restriction_crud.get_or_create(r, session)
                )

        requirements = []
        if purchase_obj.requirements is not None:
            for r in purchase_obj.requirements:
                requirements.append(
                    await requirement_crud.get_or_create(r, session)
                )

        await purchase_crud.append_add_info(
            purchase_db, preferences, requirements, restrictions, session
        )

    await callback.message.edit_reply_markup(
        reply_markup=delete_subscription_button
    )
    # DB add error
    await callback.answer(text=SUBSCRIPTION_ADDED)


@router.callback_query(F.data == 'delete_subscription')
async def delete_subscritpion(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        num = get_purchase_num_form_message(callback.message.text)
        purchase = await purchase_crud.get_purchase_by_number(num, session)
        user = await user_crud.get_user_by_chat_id(
            callback.from_user.id, session)
        await purchase_crud.delete_subscription(purchase, user, session)
    await callback.message.edit_reply_markup(
        reply_markup=add_subscription_button
    )
    await callback.answer(text=SUBSCRIPTION_DELETED)
