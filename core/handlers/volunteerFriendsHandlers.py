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
    volunteerFoodInfo = (await request.getVolunteerFoodById(volunteerId))[0]
    await state.update_data(toId=volunteerId)
    await state.update_data(food = volunteerFoodInfo)
    print(volunteerFoodInfo)
    print(findOutAmountOfFoodVolunteer('dry_dog_food', state))
    await message.answer_photo(caption=messageToSend, photo=photo_id, reply_markup=gеt_volunteer_keyboard())

@router.callback_query(F.data == 'volGiveFood')
async def volGiveFood(call: CallbackQuery, request: Request, state: FSMContext):
    await state.set_state(VolFriends.GET_RAW_CAT_FOOD)
    await call.message.answer("Введите количество сырого кошачьего корма", reply_markup=gеt_go_menu_keyboard())

@router.message(VolFriends.GET_RAW_CAT_FOOD, F.text)
async def getRawCatFood(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('dry_dog_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(raw_cat_food=message.text)
        await state.set_state(VolFriends.GET_DRY_CAT_FOOD)
        await message.answer(text="Введите количество сухого кошачьего корма", reply_markup=gеt_go_menu_keyboard())



@router.message(VolFriends.GET_DRY_CAT_FOOD, F.text)
async def getDryCatFood(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('dry_dog_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(dry_cat_food=message.text)
        await state.set_state(VolFriends.GET_RAW_DOG_FOOD)
        await message.answer(text="Введите количество сырого собачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(VolFriends.GET_RAW_DOG_FOOD, F.text)
async def getRawDogFood(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('dry_dog_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(raw_dog_food=message.text)
        await state.set_state(VolFriends.GET_DRY_DOG_FOOD)
        await message.answer(text="Введите количество сухого собачьего корма", reply_markup=gеt_go_menu_keyboard())


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



@router.message(VolFriends.GET_PHOTO, F.photo)
async def getPhotoOrder(message: Message, state: FSMContext, request: Request):
    await state.update_data(photos=getAllPhotosIds(message.photo))
    await state.update_data(volunteer_id=message.from_user.id)
    order_data = await state.get_data()

    await request.addNewOrder(message.from_user.id, order_data)
    for photo_id in order_data['photos']:
        await request.InsertNewPhoto(photo_id)
    await message.answer(text="Отлично! Удачной доставки!", reply_markup=gеt_go_menu_keyboard())

    await request.updatePointFood(dict(foodType='dry_cat_food', foodVolume=order_data['dry_cat_food'],
                                       pointId=order_data['pointId']), "decrease")
    await request.updatePointFood(dict(foodType='wet_cat_food', foodVolume=order_data['raw_cat_food'],
                                       pointId=order_data['pointId']), "decrease")
    await request.updatePointFood(dict(foodType='dry_dog_food', foodVolume=order_data['dry_dog_food'],
                                       pointId=order_data['pointId']), "decrease")
    await request.updatePointFood(dict(foodType='wet_dog_food', foodVolume=order_data['raw_dog_food'],
                                       pointId=order_data['pointId']), "decrease")

    await request.upgradeVolunteerFoodBalance(dict(foodType='dry_cat_food', foodVolume=order_data['dry_cat_food'],
                                       volunteer_id=order_data['volunteer_id']), "increase")
    await request.upgradeVolunteerFoodBalance(dict(foodType='raw_cat_food', foodVolume=order_data['raw_cat_food'],
                                       volunteer_id=order_data['volunteer_id']), "increase")
    await request.upgradeVolunteerFoodBalance(dict(foodType='dry_dog_food', foodVolume=order_data['dry_dog_food'],
                                       volunteer_id=order_data['volunteer_id']), "increase")
    await request.upgradeVolunteerFoodBalance(dict(foodType='raw_dog_food', foodVolume=order_data['raw_dog_food'],
                                       volunteer_id=order_data['volunteer_id']), "increase")



async def findOutAmountOfFoodVolunteer(type, state: FSMContext):
    data = await state.get_data()
    return int(data['food'][type])



# @router.message(VolFriends.GIVE_FOOD, F.text)
# async def giveFood(message: Message, request: Request, state: FSMContext, bot: Bot):
#     await state.set_state(None)
#     data = await state.get_data()
#     await bot.send_message(chat_id=data['toId'], text=f"Вам пришел запрос от {message.from_user.id} чтобы передать вам {message.text}кг корма!", reply_markup=gеt_accept_keyboard(message.from_user.id, data['toId'], message.text))
#     await message.answer("Запрос отправлен!", reply_markup=gеt_go_menu_keyboard())

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