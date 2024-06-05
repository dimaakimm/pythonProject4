import json
from aiogram import Bot
from aiogram.types import Message
from core.keyboards.inline import get_inline_start_keyboard
from core.keyboards.reply import reply_keyboard, loc_tel_poll_keyboard, get_reply_keyboard
from core.handlers.callback import select_category
async def get_start(message: Message, bot: Bot):
    await message.answer(f'<b>Привет, {message.from_user.first_name}!\nМожешь ознакомиться с нашим проектом)</b>)', reply_markup=get_inline_start_keyboard())

async def get_location(message: Message, bot: Bot):
    await message.answer('You have send your location!\r\a'
                         f'{message.location.latitude}\r\n{message.location.longitude}')


async def get_photo(message: Message, bot: Bot):
    await message.answer(f'Nice one! You have sent an image. Ill save it')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, str(message.from_user.id) + 'photo.jpg')

