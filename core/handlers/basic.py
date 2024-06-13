from aiogram import F, Router
from aiogram.types import Message
from core.utils.dbConnection import Request
from aiogram.filters import Command
from core.keyboards.inline import getInlineStartVolunteerKeyBoard, gеtStartKeyboard, getInlineStartAdminKeyBoard
from aiogram.types import CallbackQuery
router = Router()

@router.message(Command(commands=['start']))
async def startBotMessage(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!\nВойди как админ/волонтер!))',
                         reply_markup=gеtStartKeyboard())


@router.callback_query(F.data == 'loginAsAdmin')
async def loginAsAdmin(call: CallbackQuery, request: Request):
    if await request.varifyAdmin(call.from_user.id):
        await call.message.answer(f'Привет, {call.from_user.first_name}!\nЭто админ бот, который поможет тебе '
                         f'обрабатывать заявки пользователей, желающих покормить животных!))',
                         reply_markup=getInlineStartAdminKeyBoard())
    else:
        await call.message.answer(f'Тебя нет в списке админов(',
                                  reply_markup=gеtStartKeyboard())

@router.callback_query(F.data == 'loginAsVolunteer')
async def loginAsVolunteer(call: CallbackQuery, request: Request):
    if (await request.varifyVolunteer(call.from_user.id)):
        await call.message.answer(f'<b>Привет, {call.from_user.first_name}!\nТы вошел как волонтер!</b>)', reply_markup=getInlineStartVolunteerKeyBoard())
    else:
        await call.message.answer(f'Тебя нет в списке волонтеров(',
                                  reply_markup=gеtStartKeyboard())


