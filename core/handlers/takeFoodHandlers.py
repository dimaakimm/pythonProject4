from aiogram import Router, F
from aiogram.filters import Command
from core.utils.dbConnection import Request
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import TakeFoodSteps
from core.keyboards.inline import gеt_go_menu_keyboard

router = Router()


@router.callback_query(F.data == "takeFood")
async def choosePointForTake(call: CallbackQuery, state: FSMContext, request: Request):
    await state.set_state(TakeFoodSteps.GET_RAW_CAT_FOOD)
    volunteerInfo = await request.showProfile(call.from_user.id)
    if (volunteerInfo[0]['state'] == "wait"):
        await call.message.answer(text="Текущих заказов нет!", reply_markup=gеt_go_menu_keyboard())
        return
    pointInfo = await request.showPointInfo(volunteerInfo[0]['point_id'])
    await state.update_data(pointId=volunteerInfo[0]['point_id'])
    for record in pointInfo:
        await state.update_data(pointInfo=record)
        await call.message.answer(f"На точке по адресу {record['address']}:\n"
                                  f"{record['wet_cat_food']} кг влажного кошачьего корма\n"
                                  f"{record['dry_cat_food']} кг сухого кошачьего корма\n"
                                  f"{record['wet_dog_food']} кг влажного собачьего корма\n"
                                  f"{record['dry_dog_food']} кг сухого собачьего корма\n")
    await call.message.answer(text="Введите количество сырого кошачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_RAW_CAT_FOOD, F.text)
async def getRawCatFood(message: Message, state: FSMContext):
    kgFoodOnPoint = int(await findOutAmountOfFoodatPointof('wet_cat_food', state))
    if (int(message.text) > kgFoodOnPoint):
        await message.answer(
            text=f"Такого количества нет, на точке только {kgFoodOnPoint} кг корма !\nПовторите ввод",
            reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(raw_cat_food=message.text)
        await state.set_state(TakeFoodSteps.GET_DRY_CAT_FOOD)
        await message.answer(text="Введите количество сухого кошачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_DRY_CAT_FOOD, F.text)
async def getDryCatFood(message: Message, state: FSMContext):
    kgFoodOnPoint = int(await findOutAmountOfFoodatPointof('dry_cat_food', state))
    if (int(message.text) > kgFoodOnPoint):
        await message.answer(text=f"Такого количества нет, на точке только {kgFoodOnPoint} кг корма !\nПовторите ввод", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(dry_cat_food=message.text)
        await state.set_state(TakeFoodSteps.GET_RAW_DOG_FOOD)
        await message.answer(text="Введите количество сырого собачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_RAW_DOG_FOOD, F.text)
async def getRawDogFood(message: Message, state: FSMContext):
    kgFoodOnPoint = int(await findOutAmountOfFoodatPointof('wet_dog_food', state))
    if (int(message.text) > kgFoodOnPoint):
        await message.answer(
            text=f"Такого количества нет, на точке только {kgFoodOnPoint} кг корма !\nПовторите ввод",
            reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(raw_dog_food=message.text)
        await state.set_state(TakeFoodSteps.GET_DRY_DOG_FOOD)
        await message.answer(text="Введите количество сухого собачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_DRY_DOG_FOOD, F.text)
async def getDryDogFood(message: Message, state: FSMContext):
    kgFoodOnPoint = int(await findOutAmountOfFoodatPointof('dry_dog_food', state))
    if (int(message.text) > kgFoodOnPoint):
        await message.answer(text=f"Такого количества нет, на точке только {kgFoodOnPoint} кг корма !\nПовторите ввод", reply_markup=gеt_go_menu_keyboard())
    else:
        await state.update_data(dry_dog_food=message.text)
        await state.set_state(TakeFoodSteps.GET_PHOTO)
        await message.answer(text="Отлично! Данные успешно заполнены!\n"
                              "Отправьте фото вашего заказа!", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_PHOTO, F.photo)
async def getPhotoOrder(message: Message, state: FSMContext, request: Request):
    await state.update_data(photo_id=message.photo[-1].file_id)
    order_data = await state.get_data()
    await request.addNewOrder(message.from_user.id, order_data)
    await message.answer(text="Отлично! Удачной доставки!", reply_markup=gеt_go_menu_keyboard())

    await request.updatePointFood(dict(foodType='dry_cat_food', foodVolume=order_data['dry_cat_food'],
                                       pointId=order_data['pointId']), "decrease")
    await request.updatePointFood(dict(foodType='wet_cat_food', foodVolume=order_data['raw_cat_food'],
                                       pointId=order_data['pointId']), "decrease")
    await request.updatePointFood(dict(foodType='dry_dog_food', foodVolume=order_data['dry_dog_food'],
                                       pointId=order_data['pointId']), "decrease")
    await request.updatePointFood(dict(foodType='wet_dog_food', foodVolume=order_data['raw_dog_food'],
                                       pointId=order_data['pointId']), "decrease")
    await request.updateVolunteerGetOrderStatus(message.from_user.id, "wait")
    await state.clear()


async def findOutAmountOfFoodatPointof(type, state: FSMContext):
    data = await state.get_data()
    return int(data['pointInfo'][type])
