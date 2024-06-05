from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало'
        ),
        BotCommand(
            command='help',
            description='Помочь'
        ),
        BotCommand(
            command='cancel',
            description='Сбросить'
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())