from aiogram import Router, F
from core.utils.callbackFactories import AddFoodToPoint
from core.utils.dbConnection import Request
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import AddFoodToPointSteps, EditPointsSteps
from core.keyboards.inline import (getInlineKeyboardPointInfo, getInlineKeyboardPointFoodType,
                                   getGoAdmiMenyKeyBoard, getInlineKeyboardPointAddAnotherFood,
                                   getInlineKeyboardPointsList, showPointsSettingsList, getGoAdminMenyKeyBoard,
                                   goSettingsPointKeyboard)

router = Router()


@router.callback_query(F.data == "getPointsSettingsList")
async def getPointsSettingsList(call: CallbackQuery):
    await call.message.answer(text='Здесь, вы можете заниматься обновлением и созданием новых точек',
                              reply_markup=showPointsSettingsList())


@router.callback_query(F.data == "addNewPoint")
async def stepPointDistrict(call: CallbackQuery, state: FSMContext, request: Request):
    districtsInfo = ('1 - Центральный административный округ (ЦАО)\n'
                     '2 - Западный административный округ (ЗАО)\n'
                     '3 - Северо-Западный административный округ (СЗАО)\n'
                     '4 - Северный административный округ (САО)\n'
                     '5 - Северо-Восточный административный округ (СВАО)\n'
                     '6 - Восточный административный округ (ВАО)\n'
                     '7 - Юго-Восточный административный округ (ЮВАО)\n'
                     '8 - Южный административный округ (ЮАО)\n'
                     '9 - Юго-Западный административный округ (ЮЗАО)')
    await call.message.answer(text='Введите округ(введите соответствующий номер)\n' + districtsInfo, reply_markup=goSettingsPointKeyboard())
    await state.set_state(EditPointsSteps.GET_POINT_DISTRICT)
    await state.update_data(point_action=call.data)


@router.callback_query(F.data == "changePointInfo")
async def stepPointDistrict(call: CallbackQuery, state: FSMContext):
    districtsInfo = ('1 - Центральный административный округ (ЦАО)\n'
                     '2 - Западный административный округ (ЗАО)\n'
                     '3 - Северо-Западный административный округ (СЗАО)\n'
                     '4 - Северный административный округ (САО)\n'
                     '5 - Северо-Восточный административный округ (СВАО)\n'
                     '6 - Восточный административный округ (ВАО)\n'
                     '7 - Юго-Восточный административный округ (ЮВАО)\n'
                     '8 - Южный административный округ (ЮАО)\n'
                     '9 - Юго-Западный административный округ (ЮЗАО)')
    await call.message.answer(text='Введите округ(введите соответствующий номер)\n' + districtsInfo, reply_markup=goSettingsPointKeyboard())
    await state.set_state(EditPointsSteps.GET_POINT_DISTRICT)
    await state.update_data(point_action=call.data)


@router.message(EditPointsSteps.GET_POINT_DISTRICT, F.text)
async def stepPointAddress(message: Message, state: FSMContext):
    await state.update_data(point_district=message.text)
    await state.set_state(EditPointsSteps.GET_POINT_ADDRESS)
    await message.answer(text='Введите адрес точки', reply_markup=goSettingsPointKeyboard())


@router.message(EditPointsSteps.GET_POINT_ADDRESS, F.text)
async def stepPointAdd(message: Message, state: FSMContext, request: Request):
    await state.update_data(point_address=message.text)
    pointData = await state.get_data()
    if pointData["point_action"] == "addNewPoint":
        await request.insertNewPoint(data=pointData)
        await message.answer('Точка добавлена!', reply_markup=goSettingsPointKeyboard())
    elif pointData["point_action"] == "changePointInfo":
        await request.editPointInfo(data=pointData)
        await message.answer('Точка изменена!', reply_markup=goSettingsPointKeyboard())
    await state.clear()


@router.callback_query(F.data == "editPoint")
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
        districtInfo = await request.getDistrictsInfo(record['id_district'])
        await call.message.answer(f"Информация по точке\n\n"
                                  f"Округ: {districtInfo[0]['name']}\n"
                                  f"Адрес: {record['address']}:\n"
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