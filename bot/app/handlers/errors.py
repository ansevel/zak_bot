from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message

from app.constants.errors_messages import REQUEST_ERROR_MESSAGE
from app.core.exceptions import ParserConnectError

router = Router()


@router.errors(ExceptionTypeFilter)
async def parser_request_error(event: ErrorEvent, message: Message):
    await message.answer(text=REQUEST_ERROR_MESSAGE)