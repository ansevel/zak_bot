from aiogram import Router
from aiogram.types import Message

from app.constants.info_messages import UNKNOWN_COMMAND

router = Router()


@router.message()
async def unknown_command_process(message: Message):
    await message.answer(text=UNKNOWN_COMMAND)
