from aiogram import Router, F
from aiogram.filters import Command
from core.utils.dbConnection import Request
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import TakeFoodSteps
from core.keyboards.inline import gеt_go_menu_keyboard

router = Router()


@router.callback_query(F.data == "takeFood")
async def choosePointForTake(call: CallbackQuery, state: FSMContext):
    await state.set_state(TakeFoodSteps.GET_RAW_CAT_FOOD)
    await call.message.answer("ЗДЕСЬ БУДУТ ДАННЫЕ О КОЛИЧЕСТВЕ КОРМА НА ТОЧКЕ")
    await call.message.answer(text="Введите количество сырого кошачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_RAW_CAT_FOOD, F.text)
async def getRawCatFood(message: Message, state: FSMContext):
    # проверку на переход за пределы количества корма на точке
    await state.update_data(raw_cat_food=message.text)
    await state.set_state(TakeFoodSteps.GET_DRY_CAT_FOOD)
    await message.answer(text="Введите количество сухого кошачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_DRY_CAT_FOOD, F.text)
async def getDryCatFood(message: Message, state: FSMContext):
    # проверку на переход за пределы количества корма на точке
    await state.update_data(dry_cat_food=message.text)
    await state.set_state(TakeFoodSteps.GET_RAW_DOG_FOOD)
    await message.answer(text="Введите количество сырого собачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_RAW_DOG_FOOD, F.text)
async def getRawDogFood(message: Message, state: FSMContext):
    # проверку на переход за пределы количества корма на точке
    await state.update_data(raw_dog_food=message.text)
    await state.set_state(TakeFoodSteps.GET_DRY_DOG_FOOD)
    await message.answer(text="Введите количество сухого собачьего корма", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_DRY_DOG_FOOD, F.text)
async def getDryDogFood(message: Message, state: FSMContext):
    # проверку на переход за пределы количества корма на точке
    await state.update_data(dry_dog_food=message.text)
    await state.set_state(TakeFoodSteps.GET_PHOTO)
    await message.answer(text="Отлично! Данные успешно заполнены!\n"
                              "Отправьте фото вашего заказа!", reply_markup=gеt_go_menu_keyboard())


@router.message(TakeFoodSteps.GET_PHOTO, F.photo)
async def getPhotoOrder(message: Message, state: FSMContext, request: Request):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(None)
    order_data = await state.get_data()
    await request.addNewOrder(message.from_user.id, order_data)
    await message.answer(text="Отлично! Удачной доставки!", reply_markup=gеt_go_menu_keyboard())