from aiogram import Bot, F, Router
from core.utils.dbConnection import Request
from core.keyboards.inline import getInlineStartVolunteerKeyBoard, gеt_go_menu_keyboard, getInlineKeyboardPet, gеt_pet_keyboard, gеt_volunteer_keyboard, gеt_accept_keyboard, gеtStartKeyboard, getInlineStartAdminKeyBoard
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import VolStepsFormAddPet, VolFriends
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "goMenu")
async def goMenu(call: CallbackQuery):
    await call.message.answer(f'<b>Ты в главном меню</b>',
                              reply_markup=getInlineStartVolunteerKeyBoard())

@router.callback_query(F.data == 'addPet')
async def addPet(call: CallbackQuery, state: FSMContext):
    await state.set_state(VolStepsFormAddPet.GET_NAME)
    await call.message.answer('Введите имя животного', reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_NAME, F.text)
async def addPetName(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(VolStepsFormAddPet.GET_INFO)
    await message.answer(f"Введите иформацию о животном", reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_INFO, F.text)
async def addPetName(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await state.set_state(VolStepsFormAddPet.GET_PHOTO)
    await message.answer(f"Пришлите фото животного", reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_PHOTO, F.photo)
async def addPetName(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    print(message.photo[-1].file_id)
    await state.set_state(VolStepsFormAddPet.GET_STERILIZED)
    form_data = await state.get_data()
    await message.answer(f"Имя: {form_data['name']}\nИнформация: {form_data['info']}\nСтерилизовано ли животное?\n1 - yes\n2 - no", reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_STERILIZED,  F.text=="1")
async def addPetName(message: Message, state: FSMContext):
    await state.update_data(is_sterilized="true")
    await state.set_state(VolStepsFormAddPet.GET_DISTRICT)
    form_data = await state.get_data()
    await message.answer(f"Имя: {form_data['name']}\nИнформация: {form_data['info']}\nСтерилизована: {form_data['is_sterilized']} \nНапишите свой район", reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_STERILIZED,  F.text=="2")
async def addPetName(message: Message, state: FSMContext):
    await state.update_data(is_sterilized="false")
    await state.set_state(VolStepsFormAddPet.GET_DISTRICT)
    form_data = await state.get_data()
    await message.answer(f"Имя: {form_data['name']}\nИнформация: {form_data['info']}\nСтерилизована: {form_data['is_sterilized']} \nНапишите свой район", reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_DISTRICT, F.text)
async def addPetName(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(VolStepsFormAddPet.GET_CONFIRM)
    form_data = await state.get_data()
    await message.answer_photo(caption = f"В анкете все верно?\n1 -yes\nИмя: {form_data['name']}\nИнформация: {form_data['info']}\nСтерилизована: {form_data['is_sterilized']} \nРайон: {form_data['district']}\n", photo = form_data['photo_id'], reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_CONFIRM, F.text=="1")
async def addPetName(message: Message, state: FSMContext, request: Request):
    await state.set_state(None)
    form_data = await state.get_data()
    await request.add_data_pet(form_data, message.from_user.id)
    await message.answer(text = f"Вы успешно добавили питомца!", reply_markup=gеt_go_menu_keyboard())
    await state.clear()


@router.callback_query(F.data == 'showProfile')
async def aboutUs(call: CallbackQuery, request: Request):
    messageToSend = showVolunteerProfileMessage(await request.showProfile(call.from_user.id))[0]
    photo_id = showVolunteerProfileMessage(await request.showProfile(call.from_user.id))[1]
    await call.message.answer_photo(caption=messageToSend, photo=photo_id, reply_markup=gеt_go_menu_keyboard())


@router.callback_query(F.data == 'showPets')
async def aboutUs(call: CallbackQuery, request: Request):
    await call.message.answer(text='Вот ваши животные!', reply_markup=getInlineKeyboardPet(await request.showVolunteersPets(call.from_user.id)))

@router.callback_query(F.data == 'findProfile')
async def aboutUs(call: CallbackQuery, state: FSMContext, request: Request):
    await state.set_state(VolFriends.GET_PROFILE)
    await call.message.answer(text="Введить id пользователя!\n(можете спросить у него)",
                              reply_markup=gеt_go_menu_keyboard())

@router.message(F.text, VolFriends.GET_PROFILE)
async def aboutUs(message: Message, state: FSMContext, request: Request):
    messageToSend = showVolunteerProfileMessage(await request.showProfile(message.text))[0]
    photo_id = showVolunteerProfileMessage(await request.showProfile(message.text))[1]
    volunteerId = showVolunteerProfileMessage(await request.showProfile(message.text))[2]
    await state.update_data(toId=volunteerId)
    await message.answer_photo(caption = messageToSend, photo = photo_id, reply_markup=gеt_volunteer_keyboard())

@router.callback_query(F.data=='volGiveFood')
async def aboutUs(call: CallbackQuery, request: Request, state: FSMContext):
    await state.set_state(VolFriends.GIVE_FOOD)
    await call.message.answer("Сколько кг корма хотите передаеть ему/ей? (целые значения)", reply_markup=gеt_go_menu_keyboard())


@router.callback_query(F.data.startswith("accept"))
async def aboutUs(call: CallbackQuery, request: Request, bot: Bot):
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

@router.callback_query(F.data.startswith("decline"))
async def aboutUs(call: CallbackQuery, request: Request, bot: Bot):
    symbIndex = call.data.index('-')
    from_id = call.data[6: symbIndex]
    to_id = call.data[symbIndex+1:]
    await call.message.answer(text="Успешно!", reply_markup=gеt_go_menu_keyboard())
    await bot.send_message(chat_id=from_id, text=f"Волонтер {to_id} отклонил ваш запрос!")



@router.message(VolFriends.GIVE_FOOD, F.text)
async def aboutUs(message: Message, request: Request, state: FSMContext, bot: Bot):
    await state.set_state(None)
    data = await state.get_data()
    await bot.send_message(chat_id=data['toId'], text=f"Вам пришел запрос от {message.from_user.id} чтобы передать вам {message.text}кг корма!", reply_markup=gеt_accept_keyboard(message.from_user.id, data['toId'], message.text))
    await message.answer("Запрос отправлен!", reply_markup=gеt_go_menu_keyboard())

@router.callback_query(F.data.startswith('showAPet'))
async def aboutUs(call: CallbackQuery, request: Request):
    pet_id = call.data[8:]
    messageToSend = takeVoluneersPet(await request.showPetProfile(pet_id))[0]
    photo_id = takeVoluneersPet(await request.showPetProfile(pet_id))[1]
    await call.message.answer_photo(photo = photo_id,
        caption= messageToSend, reply_markup=gеt_pet_keyboard(pet_id))

@router.callback_query(F.data.startswith('petDelete'))
async def aboutUs(call: CallbackQuery, request: Request):
    pet_id = call.data[9:]
    await request.delete_data_pet(pet_id)
    await call.message.answer(text="Удален!", reply_markup=gеt_go_menu_keyboard())


def getAllRequestsMessage(allRequests):
    message = "ЗАЯВКИ:\n"
    message += "-------------------------------------------\n"
    for record in allRequests:
        message += f"name: {record['name']}\nsurname: {record['surname']}\nemail: {record['email']}\nphone: {record['phone']}\n"
        message += "-------------------------------------------\n"
    return message

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

def showProfileMessage(allRequests):
    message = "ВАШ ПРОФИЛЬ:\n"
    photo_id = 0
    message += "-------------------------------------------\n"
    for record in allRequests:
        message += f"Имя: {record['forename']}\nФамилия: {record['surname']}\nId: {record['id']}\nПочта: {record['email']}\nТелефон: {record['phone_number']}\n"
        photo_id = record[photo_id]
        message += "-------------------------------------------\n"
    return [message, photo_id]

def takeVoluneersPets(allRequests):
    message = "ВАШИ ПИТОМЦЫ:\n"
    keyboard_builder = InlineKeyboardBuilder()
    for record in allRequests:
        message += f"Имя: {record['forename']}\nФамилия: {record['surname']}\nПочта: {record['email']}\nТелефон: {record['phone_number']}\n"
        message += "-------------------------------------------\n"
    return message
def takeVoluneersPet(allRequests):
    message = "ВАШ ПИТОМЕЦ:\n"
    photo_id = 0
    for record in allRequests:
        message += f"Вот ваш питомец\nИмя: {record['name']}\nИнформация: {record['info']}\nСтерилизована: {record['is_sterilized']} \nРайон: {record['district']}\n"
        photo_id = record['photo_id']
    return [message, photo_id]