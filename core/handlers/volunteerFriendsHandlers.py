from aiogram import Bot, F, Router
from core.utils.dbConnection import Request
from core.keyboards.inline import getInlineStartVolunteerKeyBoard, gеt_go_menu_keyboard, getInlineKeyboardPet, gеt_pet_keyboard, gеt_volunteer_keyboard, gеt_accept_keyboard, gеtStartKeyboard, getInlineStartAdminKeyBoard
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import VolStepsFormAddPet, VolFriends
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()

@router.callback_query(F.data == 'findProfile')
async def findProfile(call: CallbackQuery, state: FSMContext, request: Request):
    await state.set_state(VolFriends.GET_PROFILE)
    await call.message.answer(text="Введить id пользователя!\n(можете спросить у него)",
                              reply_markup=gеt_go_menu_keyboard())
    await call.answer()

@router.message(F.text, VolFriends.GET_PROFILE)
async def getProfile(message: Message, state: FSMContext, request: Request):
    messageToSend = showVolunteerProfileMessage(await request.showProfile(message.text))[0]
    photo_id = showVolunteerProfileMessage(await request.showProfile(message.text))[1]
    volunteerId = showVolunteerProfileMessage(await request.showProfile(message.text))[2]
    await state.update_data(toId=volunteerId)
    await message.answer_photo(caption=messageToSend, photo=photo_id, reply_markup=gеt_volunteer_keyboard())


@router.message(VolFriends.GIVE_FOOD, F.text)
async def giveFood(message: Message, request: Request, state: FSMContext, bot: Bot):
    await state.set_state(None)
    data = await state.get_data()
    await bot.send_message(chat_id=data['toId'], text=f"Вам пришел запрос от {message.from_user.id} чтобы передать вам {message.text}кг корма!", reply_markup=gеt_accept_keyboard(message.from_user.id, data['toId'], message.text))
    await message.answer("Запрос отправлен!", reply_markup=gеt_go_menu_keyboard())

@router.callback_query(F.data == 'volGiveFood')
async def volGiveFood(call: CallbackQuery, request: Request, state: FSMContext):
    await state.set_state(VolFriends.GIVE_FOOD)
    await call.message.answer("Сколько кг корма хотите передаеть ему/ей? (целые значения)", reply_markup=gеt_go_menu_keyboard())
    await call.answer()

@router.callback_query(F.data.startswith("accept"))
async def acceptFood(call: CallbackQuery, request: Request, bot: Bot):
    symbIndex1 = call.data.find('-')
    symbIndex2 = call.data.find('-', call.data.find('-') + 1)
    from_id = call.data[6: symbIndex1]
    to_id = call.data[symbIndex1 + 1:symbIndex2]
    volume = call.data[symbIndex2 + 1:]
    print(from_id)
    print(to_id)
    print(volume)
    await request.giveFoodFromVtoV(from_id, to_id, volume)
    await call.message.answer(text="Успешно!", reply_markup=gеt_go_menu_keyboard())
    await bot.send_message(chat_id=from_id, text=f"Волонтер {to_id} принял ваш запрос!")
    await call.answer()

@router.callback_query(F.data.startswith("decline"))
async def declineFood(call: CallbackQuery, request: Request, bot: Bot):
    symbIndex = call.data.index('-')
    from_id = call.data[6: symbIndex]
    to_id = call.data[symbIndex+1:]
    await call.message.answer(text="Успешно!", reply_markup=gеt_go_menu_keyboard())
    await bot.send_message(chat_id=from_id, text=f"Волонтер {to_id} отклонил ваш запрос!")
    await call.answer()

def showVolunteerProfileMessage(allRequests):
    message = "ПРОФИЛЬ ВОЛОНТЕРА:\n"
    photo_id = 0
    id = ""
    message += "-------------------------------------------\n"
    for record in allRequests:
        message += f"Имя: {record['forename']}\nФамилия: {record['surname']}\nId: {record['id']}\nПочта: {record['email']}\nТелефон: {record['phone_number']}\n"
        photo_id = record['photo_id']
        id = record['id']
        message += "-------------------------------------------\n"
    return [message, photo_id, id]