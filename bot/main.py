import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import settings
from app.handlers import other_handlers, user_handlers
from app.keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting the bot')

    bot = Bot(
        token=settings.telegram_api_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    await bot.delete_my_commands()
    await set_main_menu(bot)
    dp.include_routers(
        user_handlers.router,
        other_handlers.router,
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
