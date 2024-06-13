from aiogram import Bot, F, Router
from core.utils.dbConnection import Request
from core.keyboards.inline import getInlineStartVolunteerKeyBoard, gеt_go_menu_keyboard, getInlineKeyboardPet, gеt_pet_keyboard, gеt_volunteer_keyboard, gеt_accept_keyboard, gеtStartKeyboard, getInlineStartAdminKeyBoard
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import VolStepsFormAddPet, VolFriends
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "goVolunteerMenu")
async def goVolunteerMenu(call: CallbackQuery):
    await call.message.answer(f'<b>Ты в главном меню</b>',
                              reply_markup=getInlineStartVolunteerKeyBoard())


@router.callback_query(F.data == 'showProfile')
async def showProfile(call: CallbackQuery, request: Request):
    messageToSend = showVolunteerProfileMessage(await request.showProfile(call.from_user.id))[0]
    photo_id = showVolunteerProfileMessage(await request.showProfile(call.from_user.id))[1]
    await call.message.answer_photo(caption=messageToSend, photo=photo_id, reply_markup=gеt_go_menu_keyboard())


@router.callback_query(F.data == 'showPets')
async def showPets(call: CallbackQuery, request: Request):
    await call.message.answer(text='Вот ваши животные!', reply_markup=getInlineKeyboardPet(await request.showVolunteersPets(call.from_user.id)))

@router.callback_query(F.data.startswith('showAPet'))
async def showAPet(call: CallbackQuery, request: Request):
    pet_id = call.data[8:]
    messageToSend = takeVoluneersPet(await request.showPetProfile(pet_id))[0]
    photo_id = takeVoluneersPet(await request.showPetProfile(pet_id))[1]
    await call.message.answer_photo(photo=photo_id,
        caption=messageToSend, reply_markup=gеt_pet_keyboard(pet_id))


@router.callback_query(F.data.startswith('petDelete'))
async def petDelete(call: CallbackQuery, request: Request):
    pet_id = call.data[9:]
    await request.delete_data_pet(pet_id)
    await call.message.answer(text="Удален!", reply_markup=gеt_go_menu_keyboard())


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