from aiogram import Router, F
from aiogram.filters import Command
from core.utils.dbConnection import Request
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import DeliveryFoodSteps
from core.keyboards.inline import gеt_go_menu_keyboard

router = Router()


@router.callback_query(F.data == "deliveryFood")
async def delivery(call: CallbackQuery, state: FSMContext, request: Request):
    await state.set_state(DeliveryFoodSteps.GET_DRY_CAT_FOOD)
    requestBalance = await request.showVolunteerBalance(call.from_user.id)
    await state.update_data(id=call.from_user.id,
                            dry_cat_food=requestBalance[0]['dry_cat_food'],
                            raw_cat_food=requestBalance[0]['raw_cat_food'],
                            dry_dog_food=requestBalance[0]['dry_dog_food'],
                            raw_dog_food=requestBalance[0]['raw_dog_food'],
                            dry_cat_food_delivery=0,
                            raw_cat_food_delivery=0,
                            dry_dog_food_delivery=0,
                            raw_dog_food_delivery=0)
    message = "У тебя есть:\n"
    for record in requestBalance:
        message += (
            f"Сухого корма для кошек: {record['dry_cat_food']}г\n"
            f"Влажного корма для кошек: {record['raw_cat_food']}г\n"
            f"Сухого корма для собак: {record['dry_dog_food']}г\n"
            f"Влажного корма для собак: {record['raw_dog_food']}г\n")
    await call.message.answer(text=message)
    await call.message.answer("Напишите, сколько граммов сухого кошачьего корма вы доставили")


@router.message(DeliveryFoodSteps.GET_DRY_CAT_FOOD, F.text)
async def getDryCatFoodDelivery(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('dry_cat_food', state))
    if int(message.text) > kgFoodVolunteerhas:
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(dry_cat_food=kgFoodVolunteerhas - int(message.text))
        await state.update_data(dry_cat_food_delivery=int(message.text))
        await state.set_state(DeliveryFoodSteps.GET_RAW_CAT_FOOD)
        await message.answer(text="Отлично! Данные успешно заполнены!\n"
                                  "Напишите, сколько граммов сырого кошачьего корма вы доставили",
                             reply_markup=gеt_go_menu_keyboard())


@router.message(DeliveryFoodSteps.GET_RAW_CAT_FOOD, F.text)
async def getRawCatFoodDelivery(message: Message, state: FSMContext):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('raw_cat_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(raw_cat_food=kgFoodVolunteerhas - int(message.text))
        await state.update_data(raw_cat_food_delivery=int(message.text))
        await state.set_state(DeliveryFoodSteps.GET_DRY_DOG_FOOD)
        await message.answer(text="Отлично! Данные успешно заполнены!\n"
                                  "Напишите, сколько граммов сухого собачьего корма вы доставили",
                             reply_markup=gеt_go_menu_keyboard())


@router.message(DeliveryFoodSteps.GET_DRY_DOG_FOOD, F.text)
async def getDryDogFoodDelivery(message: Message, state: FSMContext, request: Request):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('dry_dog_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(dry_dog_food=kgFoodVolunteerhas - int(message.text))
        await state.update_data(dry_dog_food_delivery=int(message.text))
        await state.set_state(DeliveryFoodSteps.GET_RAW_DOG_FOOD)
        await message.answer(text="Отлично! Данные успешно заполнены!\n"
                                  "Напишите, сколько граммов сырого собачьего корма вы доставили",
                             reply_markup=gеt_go_menu_keyboard())


@router.message(DeliveryFoodSteps.GET_RAW_DOG_FOOD, F.text)
async def getRawDogFoodDelivery(message: Message, state: FSMContext, request: Request):
    kgFoodVolunteerhas = int(await findOutAmountOfFoodVolunteer('raw_dog_food', state))
    if (int(message.text) > kgFoodVolunteerhas):
        await message.answer(text=f"Такого количества корма у вас нет", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(raw_dog_food=kgFoodVolunteerhas - int(message.text))
        await state.update_data(raw_dog_food_delivery=int(message.text))
        await state.set_state(DeliveryFoodSteps.GET_COMMENT)
        await message.answer(text="Отлично! Данные успешно заполнены!\n"
                                  "Отправьте комментарий к вашему заказу!", reply_markup=gеt_go_menu_keyboard())


@router.message(DeliveryFoodSteps.GET_COMMENT, F.text)
async def getCommentDelivery(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(DeliveryFoodSteps.GET_PHOTO)
    await message.answer(text="Теперь отправьте фото подтверждение!", reply_markup=gеt_go_menu_keyboard())


@router.message(DeliveryFoodSteps.GET_PHOTO, F.photo)
async def getPhotoDelivery(message: Message, state: FSMContext, request: Request):
    await state.update_data(photos=getAllPhotosIds(message.photo))
    await state.set_state(DeliveryFoodSteps.DONE)
    order_data = await state.get_data()
    await state.clear()

    await request.addNewOrderDelivery(message.from_user.id, order_data)
    for photo_id in order_data['photos']:
        await request.InsertNewPhotoDelivery(photo_id)
    await request.updateFoodVolunteer(message.from_user.id, order_data['raw_cat_food'], order_data['dry_cat_food'],
                                      order_data['raw_dog_food'],
                                      order_data['dry_dog_food'])
    await message.answer(text="Фотографии успешно добавлены\nСпасибо, что доставили корм!",
                         reply_markup=gеt_go_menu_keyboard())


async def findOutAmountOfFoodVolunteer(type, state: FSMContext):
    data = await state.get_data()
    return int(data[type])


def getAllPhotosIds(photos):
    photoIds = []
    for photo in photos:
        photoIds.append(photo.file_id)
    return photoIds