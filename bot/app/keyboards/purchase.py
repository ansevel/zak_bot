from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.core.db import AsyncSessionLocal
from app.crud.purchase import purchase_crud

add_subscription_button = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text='➕ Добавить в отслеживаемые',
                             callback_data='add_subscription')
    ]]
)

delete_subscription_button = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text='❌ Убрать из отслеживаемых',
                             callback_data='delete_subscription',)
    ]]
)


async def get_inline_button(number: str, user_id) -> InlineKeyboardMarkup:
    return add_subscription_button
