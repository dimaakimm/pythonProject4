from aiogram import Bot, Dispatcher
import asyncio
import logging
from core.handlers.basic import router
from core.settings import settings
import asyncpg
from core.middlewares.db import DbSession

dp = Dispatcher()
bot = Bot(token=settings.bots.bot_token)
bot.parse_mode = 'HTML'


async def start():
    try:
        dp.include_router(router)
        pool_connect = await asyncpg.create_pool(user='postgres', password='007787898',
                                                 database='users_bd', port=5432, command_timeout=60)
        dp.update.middleware.register(DbSession(pool_connect))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    asyncio.run(start())
