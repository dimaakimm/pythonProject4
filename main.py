import asyncio
import asyncpg
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties

from core.settings import settings
from core.middlewares.db import DbSession

from core.handlers import (basic, volunteerHandlers, adminHandlers, addPetHandlers, addAdminHandlers,
                           addVolunteerHandlers, volunteerFriendsHandlers,
                           feedPetsHandlers, takeFoodHandlers, volunteerOrder, addFoodToPoint)
import logging


async def start():
    dp = Dispatcher()
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
    try:
        dp.include_router(basic.router)
        dp.include_router(adminHandlers.router)
        dp.include_router(volunteerHandlers.router)
        dp.include_router(addPetHandlers.router)
        dp.include_router(addAdminHandlers.router)
        dp.include_router(addVolunteerHandlers.router)
        dp.include_router(volunteerFriendsHandlers.router)
        dp.include_router(volunteerOrder.router)
        dp.include_router(takeFoodHandlers.router)
        dp.include_router(feedPetsHandlers.router)
        dp.include_router(addFoodToPoint.router)
        pool_connect = await asyncpg.create_pool(host=settings.db.host, user=settings.db.user,
                                                 password=settings.db.password, database=settings.db.database,
                                                 port=settings.db.port, command_timeout=60)
        dp.update.middleware.register(DbSession(pool_connect))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    asyncio.run(start())