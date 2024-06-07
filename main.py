from aiogram import Bot, Dispatcher
import asyncio
import logging
from core.handlers.basic import router
from core.settings import settings

dp = Dispatcher()
bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
async def start():
    try:
        dp.include_router(router)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    asyncio.run(start())

