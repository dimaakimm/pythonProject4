from aiogram import Router, F
from core.utils.callbackFactories import AddFoodToPoint
from core.utils.dbConnection import Request
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import AddFoodToPointSteps
from core.keyboards.inline import (getInlineKeyboardPointInfo, getInlineKeyboardPointFoodType,
                                   getGoAdmiMenyKeyBoard, getInlineKeyboardPointAddAnotherFood,
                                   getInlineKeyboardPointsList)

router = Router()


@router.callback_query(F.data == "getPointSettings")
async def getPointSettings(call: CallbackQuery, request: Request):
    await call.message.answer(text="Выберите нужную точку", reply_markup=getInlineKeyboardPointsList(
        await request.showPinnedPoints(call.from_user.id)
    ))


@router.callback_query(F.data.startswith('showPointInfo'))
async def showPointInfo(call: CallbackQuery, request: Request, state: FSMContext):
    await state.set_state(AddFoodToPointSteps.START)
    pointInfo = await request.showPointInfo(call.data[13:])
    for record in pointInfo:
        await state.update_data(pointId=record['id'])
        await call.message.answer(f"На точке по адресу {record['address']}:\n"
                                  f"{record['dry_cat_food']}г сухого корма для кошек\n"
                                  f"{record['wet_cat_food']}г влажного корма для кошек\n"
                                  f"{record['dry_dog_food']}г сухого корма для собак\n"
                                  f"{record['wet_dog_food']}г влажного корма для собак\n",
                                  reply_markup=getInlineKeyboardPointInfo())


@router.callback_query(F.data == "addFoodToPoint")
async def stepFoodType(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddFoodToPointSteps.GET_FOOD_TYPE)
    await call.message.answer(f"Какой корм нужно добавить?",
                              reply_markup=getInlineKeyboardPointFoodType())


@router.callback_query(AddFoodToPoint.filter())
async def stepFoodVolume(call: CallbackQuery, callback_data: AddFoodToPoint, state: FSMContext):
    await state.update_data(foodType=callback_data.foodType)
    await state.set_state(AddFoodToPointSteps.GET_VOLUME)
    await call.message.answer(f"Введите количество корма",
                              reply_markup=getGoAdmiMenyKeyBoard())


@router.message(AddFoodToPointSteps.GET_VOLUME, F.text)
async def stepAddFoodToPointFinish(message: Message, state: FSMContext, request: Request):
    await state.update_data(foodVolume=int(message.text))
    await message.answer(f"Данные о пункте обновлены.\n",
                         reply_markup=getInlineKeyboardPointAddAnotherFood())
    user_data = await state.get_data()
    await request.updatePointFood(user_data, "increase")
