from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import CreatingAdminSteps, CreatingVolunteerSteps
from core.keyboards.inline import getInlineStartAdminKeyBoard, getInlineUserSettingsKeyboard, getGoAdmiMenyKeyBoard
from core.utils.dbConnection import Request

router = Router()

@router.callback_query(F.data == "goAdminMenu")
async def goMenu(call: CallbackQuery):
    await call.message.answer(f'<b>Ты в главном меню</b>',
                              reply_markup=getInlineStartAdminKeyBoard())

@router.message(Command(commands=['start']))
async def startBotMessage(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!\nЭто административный бот, который поможет '
                         f'контролировать процесс кормления животных. Бот позволяет администратору взаимодействовать с курьерами, '
                         f'обновлять данные пунктов хранения корма и помогать животным!))',
                         reply_markup=getInlineStartAdminKeyBoard())


@router.callback_query(F.data == "getUsersSettings")
async def userSettingsMenu(call: CallbackQuery):
    # await call.message.answer(getAllRequestsMessage(await request.getAllRequests()))
    await call.message.answer(f'Здесь, вы можете заниматься обновлением, удалением и созданием новых '
                              f'пользователей. Пользователи делятся на два типа: Админ и Волонтер. В роли админа '
                              f'вы можете использовать функционал представленных кнопок',
                              reply_markup=getInlineUserSettingsKeyboard())


def getAllRequestsMessage(allRequests):
    message = "ЗАЯВКИ:\n"
    message += "-------------------------------------------\n"
    for record in allRequests:
        message += f"name: {record['name']}\nsurname: {record['surname']}\nemail: {record['email']}\nphone: {record['phone']}\n"
        message += "-------------------------------------------\n"
    return message

@router.callback_query(F.data == "insertAdmin")
async def stepAdminId(call: CallbackQuery, state: FSMContext):
    await state.set_state(CreatingAdminSteps.GET_ID)
    await call.message.answer('Введите id нового администратора', reply_markup=getGoAdmiMenyKeyBoard())


@router.message(CreatingAdminSteps.GET_ID, F.text)
async def stepAdminFirstName(message: Message, state: FSMContext):
    await state.update_data(admin_id=message.text)
    await state.set_state(CreatingAdminSteps.GET_FIRST_NAME)
    await message.answer('Введите имя администратора', reply_markup=getGoAdmiMenyKeyBoard())


@router.message(CreatingAdminSteps.GET_FIRST_NAME, F.text)
async def stepAdminLastName(message: Message, state: FSMContext):
    await state.update_data(admin_first_name=message.text)
    await state.set_state(CreatingAdminSteps.GET_LAST_NAME)
    await message.answer('Введите фамилию администратора', reply_markup=getGoAdmiMenyKeyBoard())


@router.message(CreatingAdminSteps.GET_LAST_NAME, F.text)
async def stepAdminGetPhone(message: Message, state: FSMContext):
    await state.update_data(admin_last_name=message.text)
    await state.set_state(CreatingAdminSteps.GET_PHONE)
    await message.answer('Введите номер телефона администратора', reply_markup=getGoAdmiMenyKeyBoard())


@router.message(CreatingAdminSteps.GET_PHONE, F.text)
async def stepAdminGetPhone(message: Message, state: FSMContext):
    await state.update_data(admin_phone=message.text)
    await state.set_state(CreatingAdminSteps.GET_PHOTO)
    await message.answer('Отправьте фотографию администратора', reply_markup=getGoAdmiMenyKeyBoard())


@router.message(CreatingAdminSteps.GET_PHOTO, F.photo)
async def stepAdminGetPhoto(message: Message, state: FSMContext):
    # нужно сделать сохрание фото
    await state.update_data(admin_photo=message.photo[-1].file_id)
    await state.set_state(CreatingAdminSteps.GET_PASSPORT)
    await message.answer('Отправьте паспорт администратора', reply_markup=getGoAdmiMenyKeyBoard())

@router.message(CreatingAdminSteps.GET_PASSPORT, F.text)
async def stepAdminGetDistrict(message: Message, state: FSMContext, request: Request):
    await state.update_data(admin_passport=message.text)
    await message.answer('Анкета администратор создана')
    user_data = await state.get_data()
    await request.add_data_admin(user_data)
    await message.answer(f'Анкета администратора:\n'
                         f'Имя: {user_data["admin_first_name"]}\n'
                         f'Фамилия: {user_data["admin_last_name"]}:\n'
                         f'Фотография: {user_data["admin_photo"]}\n'
                         f'Id: {user_data["admin_id"]}\n'
                         f'Номер телефона: {user_data["admin_phone"]}\n'
                         f'Паспорт: {user_data["admin_passport"]}\n', reply_markup=getGoAdmiMenyKeyBoard())
    await state.clear()


@router.callback_query(F.data == "insertVolunteer")
async def stepVolunteerId(call: CallbackQuery, state: FSMContext):
    await state.set_state(CreatingVolunteerSteps.GET_ID)
    await call.message.answer('Введите id волонтера', reply_markup=getGoAdmiMenyKeyBoard())


@router.message(CreatingVolunteerSteps.GET_ID, F.text)
async def stepVolunteerFirstName(message: Message, state: FSMContext):
    await state.update_data(volunteer_id=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_FIRST_NAME)
    await message.answer('Введите имя волонтера', reply_markup=getGoAdmiMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_FIRST_NAME, F.text)
async def stepVolunteerLastName(message: Message, state: FSMContext):
    await state.update_data(volunteer_first_name=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_LAST_NAME)
    await message.answer('Введите фамилию волонтера', reply_markup=getGoAdmiMenyKeyBoard())


@router.message(CreatingVolunteerSteps.GET_LAST_NAME, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_last_name=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_PHONE)
    await message.answer('Введите телефон волонтера', reply_markup=getGoAdmiMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_PHONE, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_phone=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_EMAIL)
    await message.answer('Введите email волонтера', reply_markup=getGoAdmiMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_EMAIL, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_email=message.text)
    await state.set_state(CreatingVolunteerSteps.GET_PHOTO_ID)
    await message.answer('Введите фотографию волонтера', reply_markup=getGoAdmiMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_PHOTO_ID, F.photo)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_photo_id=message.photo[-1].file_id)
    await state.set_state(CreatingVolunteerSteps.GET_BALANCE)
    await message.answer('Пришлите, сколько кг корма на руках у волонтера', reply_markup=getGoAdmiMenyKeyBoard())

@router.message(CreatingVolunteerSteps.GET_BALANCE, F.text)
async def stepVolunteerGetPhone(message: Message, state: FSMContext):
    await state.update_data(volunteer_balance = message.text)
    await state.set_state(CreatingVolunteerSteps.GET_PASSPORT)
    await message.answer('Пришлите пасспорт волонтера', reply_markup=getGoAdmiMenyKeyBoard())

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
                         f'Корма на руках: {user_data["volunteer_balance"]}\n', reply_markup=getGoAdmiMenyKeyBoard()
                         )
    await state.clear()