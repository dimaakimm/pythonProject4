from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from pythonProject4.core.utils.stateForms import CreatingAdminSteps, CreatingVolunteerSteps
from pythonProject4.core.keyboards.inline import getInlineStartAdminKeyBoard, getInlineUserSettingsKeyboard


router = Router()

@router.callback_query(F.data == "getUsersSettings")
async def userSettingsMenu(call: CallbackQuery):
    # await call.message.answer(getAllRequestsMessage(await request.getAllRequests()))
    await call.message.answer(f'Здесь, вы можете заниматься обновлением, удалением и созданием новых '
                              f'пользователей. Пользователи делятся на два типа: Админ и Волонтер. В роли админа '
                              f'вы можете использовать функционал представленных кнопок',
                              reply_markup=getInlineUserSettingsKeyboard())

