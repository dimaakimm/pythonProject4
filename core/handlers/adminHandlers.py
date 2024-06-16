from aiogram import Router, F
from aiogram.filters import Command

from core.utils.callbackFactories import AddFoodToPoint
from core.utils.dbConnection import Request
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import (CreatingAdminSteps, CreatingVolunteerSteps, DeletingVolunteerSteps,
    DeletingAdminSteps, AddFoodToPointSteps)
from core.keyboards.inline import (getInlineStartAdminKeyBoard, getInlineUserSettingsKeyboard, getGoAdminMenyKeyBoard,
    getInlineKeyboardPoints, getInlineKeyboardPointInfo, getInlineKeyboardPointFoodType, getGoAdmiMenyKeyBoard,
    getInlineKeyboardPointAddAnotherFood, getInlineKeyboardPointsList)

router = Router()


@router.callback_query(F.data == "getUsersSettings")
async def userSettingsMenu(call: CallbackQuery):
    # await call.message.answer(getAllRequestsMessage(await request.getAllRequests()))
    await call.message.answer(f'Здесь, вы можете заниматься обновлением, удалением и созданием новых '
                              f'пользователей. Пользователи делятся на два типа: Админ и Волонтер. В роли админа '
                              f'вы можете использовать функционал представленных кнопок',
                              reply_markup=getInlineUserSettingsKeyboard())
    await call.answer()


@router.callback_query(F.data == "deleteAdmin")
async def getdeletedAdminId(call: CallbackQuery, state: FSMContext):
    await state.set_state(DeletingAdminSteps.GET_ID)
    await call.message.answer(text="Пришлите id админа которого хотите удалить", reply_markup=getGoAdminMenyKeyBoard())
    await call.answer()


@router.message(DeletingAdminSteps.GET_ID, F.text)
async def deleteAdmin(message: Message, state: FSMContext, request: Request):
    await state.set_state(None)
    await request.delete_data_admin(message.text)
    await message.answer(text="Удален!", reply_markup=getInlineStartAdminKeyBoard())


@router.callback_query(F.data == "deleteVolunteer")
async def getdeletedAdminId(call: CallbackQuery, state: FSMContext):
    await state.set_state(DeletingVolunteerSteps.GET_ID)
    await call.message.answer(text="Пришлите id админа которого хотите удалить", reply_markup=getGoAdminMenyKeyBoard())
    await call.answer()


@router.message(DeletingVolunteerSteps.GET_ID, F.text)
async def deleteAdmin(message: Message, state: FSMContext, request: Request):
    await state.set_state(None)
    await request.delete_data_volunteers(message.text)
    await message.answer(text="Удален!", reply_markup=getInlineStartAdminKeyBoard())


@router.callback_query(F.data == "goAdminMenu")
async def goAdminMenu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f'Привет, {call.from_user.first_name}!\nЭто админ бот, который поможет тебе '
                              f'обрабатывать заявки пользователей, желающих покормить животных!))',
                              reply_markup=getInlineStartAdminKeyBoard())

@router.callback_query(F.data == "goAdminSettings")
async def goAdminMenu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(f'Настройки пользователя',
                              reply_markup=getInlineUserSettingsKeyboard())


@router.callback_query(F.data == "getPointSettings")
async def getPointSettings(call: CallbackQuery, request: Request):
    await call.message.answer(text="Выберите нужную точку", reply_markup=getInlineKeyboardPointsList(
        await request.showPinnedPoints(call.from_user.id)
    ))
    print(request.showPinnedPoints(call.from_user.id))


@router.callback_query(F.data.startswith('showPointInfo'))
async def showPointInfo(call: CallbackQuery, request: Request, state: FSMContext):
    await state.set_state(AddFoodToPointSteps.START)
    pointInfo = await request.showPointInfo(call.data[13:])
    for record in pointInfo:
        await state.update_data(pointId=record['id'])
        await call.message.answer(f"На точке по адресу {record['address']}:\n"
                                  f"{record['dry_cat_food']} кг сухого корма для кошек\n"
                                  f"{record['wet_cat_food']} кг влажного корма для кошек\n"
                                  f"{record['dry_dog_food']} кг сухого корма для собак\n"
                                  f"{record['wet_dog_food']} кг влажного корма для собак\n",
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
    await state.clear()


