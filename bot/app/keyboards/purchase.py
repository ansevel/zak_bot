from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

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


def get_inline_button(message: Message) -> InlineKeyboardMarkup:
    #  Check purchase number in Subscription
    return add_subscription_button
