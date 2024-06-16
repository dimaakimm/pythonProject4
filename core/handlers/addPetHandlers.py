from aiogram import Bot, F, Router
from core.utils.dbConnection import Request
from core.keyboards.inline import gеt_go_menu_keyboard, petCreateSuccesfulKeyBoard, choosePetSterilized
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import VolStepsFormAddPet


router = Router()

@router.callback_query(F.data == 'addPet')
async def addPet(call: CallbackQuery, state: FSMContext):
    await state.set_state(VolStepsFormAddPet.GET_NAME)
    await call.message.answer('Введите имя животного', reply_markup=gеt_go_menu_keyboard())
    await call.answer()


@router.message(VolStepsFormAddPet.GET_NAME, F.text)
async def addPetName(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(VolStepsFormAddPet.GET_INFO)
    await message.answer(f"Введите иформацию о животном", reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_INFO, F.text)
async def addPetPhoto(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await state.set_state(VolStepsFormAddPet.GET_PHOTO)
    await message.answer(f"Пришлите фото животного", reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_PHOTO, F.photo)
async def addPetSterilized(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(VolStepsFormAddPet.GET_STERILIZED)
    await message.answer(f"Стерилизовано ли животное?", reply_markup=choosePetSterilized())

@router.callback_query(VolStepsFormAddPet.GET_STERILIZED,  F.data=="sterilized")
async def addPetName(call: CallbackQuery, state: FSMContext):
    await state.update_data(is_sterilized="true")
    await state.set_state(VolStepsFormAddPet.GET_DISTRICT)
    await call.message.answer(f"Напишите свой район", reply_markup=gеt_go_menu_keyboard())

@router.callback_query(VolStepsFormAddPet.GET_STERILIZED,  F.data=="not_sterilized")
async def addPetName(call: CallbackQuery, state: FSMContext):
    await state.update_data(is_sterilized="false")
    await state.set_state(VolStepsFormAddPet.GET_DISTRICT)
    await call.message.answer(f"Напишите свой район", reply_markup=gеt_go_menu_keyboard())

@router.message(VolStepsFormAddPet.GET_DISTRICT, F.text)
async def addPetName(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(VolStepsFormAddPet.GET_CONFIRM)
    form_data = await state.get_data()
    await message.answer_photo(caption=f"В анкете все верно?\nИмя: {form_data['name']}\nИнформация: {form_data['info']}\nСтерилизована: {form_data['is_sterilized']} \nРайон: {form_data['district']}\n", photo=form_data['photo_id'], reply_markup=petCreateSuccesfulKeyBoard())


@router.callback_query(VolStepsFormAddPet.GET_CONFIRM, F.data == "createPetSuccesful")
async def addPetName(call: CallbackQuery, state: FSMContext, request: Request):
    await state.set_state(None)
    form_data = await state.get_data()
    await request.add_data_pet(form_data, call.from_user.id)
    await call.message.answer(text=f"Вы успешно добавили питомца!", reply_markup=gеt_go_menu_keyboard())
    await call.answer()
