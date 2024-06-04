from aiogram import Bot
from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand

from app.constants.menu import HELP_COMMAND, LIST_COMMAND, START_COMMAND


async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command='start', description=START_COMMAND),
        BotCommand(command='help', description=HELP_COMMAND),
        BotCommand(command='list', description=LIST_COMMAND),
    ]
    await bot(SetMyCommands(commands=commands))
