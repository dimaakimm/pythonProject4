from aiogram import Bot, Router, F
from aiogram.filters import Command
from core.utils.dbConnection import Request
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import CreatingAdminSteps
from core.keyboards.inline import getInlineStartAdminKeyBoard, getInlineUserSettingsKeyboard, getGoAdminMenyKeyBoard, getInlineKeyboardVolunteers, getInlineKeyboardPoints


router = Router()

@router.callback_query(F.data == "getVolunteerWork")
async def getListOfVolunteers(call: CallbackQuery, request: Request):
    await call.message.answer(text='Доступные волонтеры', reply_markup=getInlineKeyboardVolunteers(await request.showVolunteersToOrder()))

@router.callback_query(F.data.startswith("orderChoose"))
async def getListOfVolunteers(call: CallbackQuery, request: Request):
    id = call.data[11:]
    await call.message.answer(text='Доступные точки', reply_markup=getInlineKeyboardPoints(await request.showPointsToOrder(), id))


@router.callback_query(F.data.startswith("orderCreate"))
async def getListOfVolunteers(call: CallbackQuery, request: Request, bot: Bot):
    index = call.data.find('-')
    volunteerId = call.data[11:index]
    pointId = call.data[index+1:]
    adress = await request.getAdressById(pointId)
    await bot.send_message(chat_id=volunteerId, text=f"Вам пришел запрос от {call.from_user.id} чтобы вы доставили корм на адрес: {adress}!")
    await call.message.answer("Запрос отправлен!", reply_markup=getGoAdminMenyKeyBoard())
