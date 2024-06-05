from aiogram.types import Message
from aiogram import Bot

async def get_true_contact(message: Message, bot: Bot):
    await message.answer(f'You have sent <b>your</b> contact {message.contact.phone_number}')

async def get_fake_contact(message: Message, bot: Bot):
    await message.answer(f'You have sent <b>not your</b> contact')