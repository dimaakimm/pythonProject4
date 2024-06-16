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
    allRequestsVol = await request.showProfile(message.text)
    requestBalance = await request.showVolunteerBalance(message.text)

    result = showVolunteerProfileMessage(allRequestsVol, requestBalance)
    messageToSend = result[0]
    photo_id = result[1]
    volunteerId = result[2]
    volunteerFoodInfo = (await request.getVolunteerFoodById(volunteerId))[0]
    await state.update_data(toId=volunteerId)
    await state.update_data(food=volunteerFoodInfo)
    await message.answer_photo(caption=messageToSend, photo=photo_id, reply_markup=gеt_volunteer_keyboard())



@router.callback_query(F.data == 'volGiveFood')
async def volGiveFood(call: CallbackQuery, request: Request, state: FSMContext):
    await state.set_state(VolFriends.GET_RAW_CAT_FOOD)
    await call.message.answer("Введите количество влажного корма для кошек (граммы)", reply_markup=gеt_go_menu_keyboard())

@router.message(VolFriends.GET_RAW_CAT_FOOD, F.text)
async def getRawCatFood(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('raw_cat_food', state))

    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(raw_cat_food=message.text)
        await state.set_state(VolFriends.GET_DRY_CAT_FOOD)
        await message.answer(text="Введите количество сухого корма для кошек (граммы)", reply_markup=gеt_go_menu_keyboard())



@router.message(VolFriends.GET_DRY_CAT_FOOD, F.text)
async def getDryCatFood(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('dry_cat_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(dry_cat_food=message.text)
        await state.set_state(VolFriends.GET_RAW_DOG_FOOD)
        await message.answer(text="Введите количество влажного корма для собак (граммы)", reply_markup=gеt_go_menu_keyboard())


@router.message(VolFriends.GET_RAW_DOG_FOOD, F.text)
async def getRawDogFood(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('raw_dog_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(raw_dog_food=message.text)
        await state.set_state(VolFriends.GET_DRY_DOG_FOOD)
        await message.answer(text="Введите количество сухого корма для собак (граммы)", reply_markup=gеt_go_menu_keyboard())


@router.message(VolFriends.GET_DRY_DOG_FOOD, F.text)
async def getDryDogFood(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('dry_dog_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(dry_dog_food=message.text)
        await state.set_state(VolFriends.GET_PHOTO)
        await message.answer(text="Отлично! Данные успешно заполнены!\n"
                              "Отправьте фото вашего заказа!", reply_markup=gеt_go_menu_keyboard())


#надо исправлять ниже
@router.message(VolFriends.GET_PHOTO, F.photo)
async def getPhotoOrder(message: Message, state: FSMContext, request: Request, bot: Bot):
    await state.set_state(None)
    data = await state.get_data()
    await bot.send_message(chat_id=data['toId'], text=f"Вам пришел запрос от {message.from_user.id} чтобы передать вам\n"
                           f"{data['raw_cat_food']}г влажного корма для кошек!\n"
                           f"{data['dry_cat_food']}г сухого корма для кошек!\n"
                           f"{data['raw_dog_food']}г влажного корма для собак!\n"
                           f"{data['dry_dog_food']}г сухого корма для собак!", reply_markup=gеt_accept_keyboard(message.from_user.id, data['toId'], data['raw_cat_food'], data['dry_cat_food'], data['raw_dog_food'], data['dry_dog_food']))
    await message.answer("Запрос отправлен!", reply_markup=gеt_go_menu_keyboard())


async def findOutAmountOfFoodVolunteer(type, state: FSMContext):
    data = await state.get_data()
    return int(data['food'][type])


@router.callback_query(F.data.startswith("accept"))
async def acceptFood(call: CallbackQuery, request: Request, bot: Bot):
    symbIndex1 = call.data.find('-')
    symbIndex2 = call.data.find('-', call.data.find('-') + 1)
    from_id = call.data[6: symbIndex1]
    to_id = call.data[symbIndex1 + 1:symbIndex2]
    volume = call.data[symbIndex2 + 1:]
    data = call.data.split('-')
    from_id = data[1]
    to_id = data[2]
    raw_cat_food = data[3]
    dry_cat_food = data[4]
    raw_dog_food = data[5]
    dry_dog_food = data[6]
    print(call.data.split('-'))
    await request.giveFoodFromVtoV(from_id, to_id, raw_cat_food, dry_cat_food, raw_dog_food, dry_dog_food)
    await call.message.answer(text="Успешно!", reply_markup=gеt_go_menu_keyboard())
    await bot.send_message(chat_id=from_id, text=f"Волонтер {to_id} принял ваш запрос!")
    await call.answer()

@router.callback_query(F.data.startswith("decline"))
async def declineFood(call: CallbackQuery, request: Request, bot: Bot):
    data = call.data.split('-')
    from_id = data[1]
    to_id = data[2]
    await call.message.answer(text="Успешно!", reply_markup=gеt_go_menu_keyboard())
    await bot.send_message(chat_id=from_id, text=f"Волонтер {to_id} отклонил ваш запрос!")
    await call.answer()

def showVolunteerProfileMessage(allRequests, requestBalance):
    message = "ПРОФИЛЬ ВОЛОНТЕРА:\n"
    photo_id = 0
    id = ""

    for record in allRequests:
        message += f"Имя: {record['forename']}\nФамилия: {record['surname']}\nId: {record['id']}\nПочта: {record['email']}\nТелефон: {record['phone_number']}\n"
    for record in requestBalance:
        message += (f"\nКоличество корма:\n"
                    f"Сухого корма для кошек: {record['dry_cat_food']}г\n"
                    f"Влажного корма для кошек: {record['raw_cat_food']}г\n"
                    f"Сухого корма для собак: {record['dry_dog_food']}г\n"
                    f"Влажного корма для собак: {record['raw_dog_food']}г\n")
    for record in allRequests:
        photo_id = record['photo_id']
        id = record['id']
    return [message, photo_id, id]