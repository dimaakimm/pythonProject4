from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import CreatingVolunteerSteps
from core.utils.dbConnection import Request
from core.keyboards.inline import getGoAdminMenyKeyBoard

router = Router()

@router.callback_query(F.data == "insertVolunteer")
async def stepVolunteerId(call: CallbackQuery, state: FSMContext):
    await state.set_state(CreatingVolunteerSteps.GET_ID)
    await call.message.answer('Введите id волонтера', reply_markup=getGoAdminMenyKeyBoard())


@router.message(CreatingVolunteerSteps.GET_ID, F.text)
async def stepVolunteerFirstName(message: Message, state: FSMContext):
    await state.update_data(volunteer_id=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_FIRST_NAME)
    await message.answer('Введите имя волонтера', reply_markup=getGoAdminMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_FIRST_NAME, F.text)
async def stepVolunteerLastName(message: Message, state: FSMContext):
    await state.update_data(volunteer_first_name=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_LAST_NAME)
    await message.answer('Введите фамилию волонтера', reply_markup=getGoAdminMenyKeyBoard())


@router.message(CreatingVolunteerSteps.GET_LAST_NAME, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_last_name=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_PHONE)
    await message.answer('Введите телефон волонтера', reply_markup=getGoAdminMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_PHONE, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_phone=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_EMAIL)
    await message.answer('Введите email волонтера', reply_markup=getGoAdminMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_EMAIL, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_email=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_PHOTO_ID)
    await message.answer('Введите фотографию волонтера', reply_markup=getGoAdminMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_PHOTO_ID, F.photo)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_photo_id=message.photo[-1].file_id)
    await state.set_state(CreatingVolunteerSteps.GET_BALANCE)
    await message.answer('Пришлите, сколько кг корма на руках у волонтера', reply_markup=getGoAdminMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_BALANCE, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_balance = message.text)
    await state.set_state(CreatingVolunteerSteps.GET_PASSPORT)
    await message.answer('Пришлите пасспорт волонтера', reply_markup=getGoAdminMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_PASSPORT, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext, request: Request):
    await state.update_data(volunteer_passport=message.text)
    await message.answer('Анкета создана')
    user_data = await state.get_data()
    await request.add_data_volunteer(user_data)
    await message.answer(f'Анкета Волонтера:\n'
                         f'id: {user_data["volunteer_id"]}\n'
                         f'Имя: {user_data["volunteer_first_name"]}\n'
                         f'Фамилия: {user_data["volunteer_last_name"]}\n'
                         f'Телефон: {user_data["volunteer_phone"]}\n'
                         f'Email: {user_data["volunteer_email"]}\n'
                         f'Паспорт: {user_data["volunteer_passport"]}\n'
                         f'photo id: {user_data["volunteer_photo_id"]}\n'
                         f'Корма на руках: {user_data["volunteer_balance"]}\n', reply_markup=getGoAdminMenyKeyBoard()
                         )
    await state.clear()