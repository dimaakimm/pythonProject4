from aiogram import Bot, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from core.utils.dbConnection import Request
from core.keyboards.inline import getInlineStartKeyBoard, gеt_go_menu_keyboard, getInlineKeyboardPet, gеt_pet_keyboard
from aiogram.types import CallbackQuery
from asyncpg import Record
from aiogram.fsm.context import FSMContext
from core.utils.statesfrom import VolStepsFormAddPet
from aiogram.utils.keyboard import InlineKeyboardBuilder
router = Router()


@router.message(Command(commands=['start']))
async def startBotMessage(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!\nЭто админ бот, который поможет тебе '
                         f'обрабатывать заявки пользователей, желающих покормить животных!))',
                         reply_markup=getInlineStartKeyBoard())
@router.callback_query(F.data == "goMenu")
async def goMenu(call: CallbackQuery):
    await call.message.answer(f'<b>Ты в главном меню</b>',
                              reply_markup=getInlineStartKeyBoard())

@router.callback_query(F.data == 'getAllRequest')
async def aboutUs(call: CallbackQuery, request: Request):
    await call.message.answer(getAllRequestsMessage(await request.getAllRequests()))


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


@router.callback_query(F.data == 'showProfile')
async def aboutUs(call: CallbackQuery, request: Request):
    await call.message.answer(showProfileMessage(await request.showProfile(call.from_user.id)))
    print(call.message.from_user.id)


@router.callback_query(F.data == 'showPets')
async def aboutUs(call: CallbackQuery, request: Request):
    await call.message.answer(text='Вот ваши животные!', reply_markup=getInlineKeyboardPet(await request.showVolunteersPets(call.from_user.id)))

@router.callback_query(F.data.startswith('showAPet'))
async def aboutUs(call: CallbackQuery, request: Request):
    pet_id = call.data[8:]
    message = takeVoluneersPet(await request.showPetProfile(pet_id))[0]
    photo_id = takeVoluneersPet(await request.showPetProfile(pet_id))[1]
    await call.message.answer_photo(photo = photo_id,
        caption= message, reply_markup=gеt_pet_keyboard(pet_id))

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


def showProfileMessage(allRequests):
    message = "ВАШ ПРОФИЛЬ:\n"
    message += "-------------------------------------------\n"
    for record in allRequests:
        message += f"Имя: {record['forename']}\nФамилия: {record['surname']}\nПочта: {record['email']}\nТелефон: {record['phone_number']}\n"
        message += "-------------------------------------------\n"
    return message

def takeVoluneersPets(allRequests):
    message = "ВАШИ ПИТОМЦЫ:\n"
    keyboard_builder = InlineKeyboardBuilder()
    for record in allRequests:
        message += f"Имя: {record['forename']}\nФамилия: {record['surname']}\nПочта: {record['email']}\nТелефон: {record['phone_number']}\n"
        message += "-------------------------------------------\n"
    return message
def takeVoluneersPet(allRequests):
    message = "ВАШ ПИТОМЕЦ:\n"
    keyboard_builder = InlineKeyboardBuilder()
    photo_id = 0
    for record in allRequests:
        message += f"Вот ваш питомец\nИмя: {record['name']}\nИнформация: {record['info']}\nСтерилизована: {record['is_sterilized']} \nРайон: {record['district']}\n"
        photo_id = record['photo_id']
    return [message, photo_id]