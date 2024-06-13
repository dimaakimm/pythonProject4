from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from pythonProject4.core.utils.stateForms import CreatingAdminSteps
from pythonProject4.core.utils.dbConnection import Request

router = Router()


@router.callback_query(F.data == "insertAdmin")
async def stepAdminId(call: CallbackQuery, state: FSMContext):
    await state.set_state(CreatingAdminSteps.GET_ID)
    await call.message.answer('Введите id нового администратора')


@router.message(CreatingAdminSteps.GET_ID, F.text)
async def stepAdminFirstName(message: Message, state: FSMContext):
    await state.update_data(admin_id=message.text)
    await state.set_state(CreatingAdminSteps.GET_FIRST_NAME)
    await message.answer('Введите имя администратора')


@router.message(CreatingAdminSteps.GET_FIRST_NAME, F.text)
async def stepAdminLastName(message: Message, state: FSMContext):
    await state.update_data(admin_first_name=message.text)
    await state.set_state(CreatingAdminSteps.GET_LAST_NAME)
    await message.answer('Введите фамилию администратора')


@router.message(CreatingAdminSteps.GET_LAST_NAME, F.text)
async def stepAdminGetPhone(message: Message, state: FSMContext):
    await state.update_data(admin_last_name=message.text)
    await state.set_state(CreatingAdminSteps.GET_PHONE)
    await message.answer('Введите номер телефона администратора')


@router.message(CreatingAdminSteps.GET_PHONE, F.text)
async def stepAdminGetPhone(message: Message, state: FSMContext):
    await state.update_data(admin_phone=message.text)
    await state.set_state(CreatingAdminSteps.GET_PHOTO)
    await message.answer('Отправьте фотографию администратора')


@router.message(CreatingAdminSteps.GET_PHOTO, F.photo)
async def stepAdminGetPhoto(message: Message, state: FSMContext):
    # нужно сделать сохрание фото
    await state.update_data(admin_photo_id=message.photo[-1].file_id)
    await state.set_state(CreatingAdminSteps.GET_PASSPORT)
    await message.answer('Отправьте паспорт администратора')


@router.message(CreatingAdminSteps.GET_PASSPORT, F.text)
async def stepAdminGetPassport(message: Message, state: FSMContext, request: Request):
    await state.update_data(admin_passport=message.text)
    await state.set_state(CreatingAdminSteps.GET_POINT)
    await message.answer('Отправьте адрес пункта, в котором работает администратор')
    await message.answer(getAllPoints(await request.getAllPoints()))


@router.message(CreatingAdminSteps.GET_POINT, F.text)
async def stepAdminGetDistrict(message: Message, state: FSMContext, request: Request):
    await state.update_data(admin_point=message.text)
    await state.set_state(CreatingAdminSteps.DONE)
    adminData = await state.get_data()
    await request.insertNewAdmin(data=adminData)
    await message.answer('Анкета администратор создана!')
    await message.answer_photo(caption=getAllAdminCardData(adminData), photo=adminData['admin_photo_id'])
    await state.clear()


def getAllPoints(allRequests):
    message = "ПУНКТЫ:\n"
    message += "----------------------------------------\n"
    for record in allRequests:
        message += f"Адрес: {record['address']}\n"
        message += "----------------------------------------\n"
    return message


def getAllAdminCardData(adminData):
    adminCard = "КАРТА АДМИНИСТАРТОРА\n\n"
    adminCard += (f"Имя: {adminData['admin_first_name']} {adminData['admin_last_name']}\n"
                  f"Номер телефона: '{adminData['admin_phone']}'\n"
                  f"Серия и номер паспорта: '{adminData['admin_passport']}'\n"
                  f"Пункт администратора: '{adminData['admin_point']}'")
    return adminCard