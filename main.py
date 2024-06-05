from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from core.filters.iscontact import IsTrueContact
import asyncio
import logging
from core.handlers.basic import get_start, get_photo, get_location
from core.settings import settings
from core.handlers.contact import get_fake_contact, get_true_contact
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from core.utils.commands import set_commands
from core.handlers.callback import select_category
class user_status(StatesGroup):
    aboutUs = State()
    choosePet = State()
async def start_bot(bot:Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='<s>Bot is on!</s>')
async def stop_bot(bot:Bot):
    await bot.send_message(settings.bots.admin_id, text='<tg-spoiler>Bot is off!</tg-spoiler>')
async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.callback_query.register(select_category)
    dp.startup.register(start_bot)
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_location, F.location)
    dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_fake_contact, F.contact)
    dp.shutdown.register(stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())

