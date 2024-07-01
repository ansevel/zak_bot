from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter

from app.core.exceptions import ParserConnectError

router = Router()


@router.errors(ExceptionTypeFilter)