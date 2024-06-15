from aiogram import Router, F, Bot
from aiogram.methods import DeleteMessage
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.stateForms import CreatingAdminSteps
from core.keyboards.inline import gеtGoSettingsAdminKeykeyboard
from core.utils.dbConnection import Request

router = Router()


@router.callback_query(F.data == "insertAdmin")
async def stepAdminId(call: CallbackQuery, state: FSMContext):
    await state.set_state(CreatingAdminSteps.GET_ID)
    await call.message.edit_text('Введите id нового администратора', reply_markup=gеtGoSettingsAdminKeykeyboard())
    await state.update_data(previousMessage=call.message)
    await call.answer()


@router.message(CreatingAdminSteps.GET_ID, F.text)
async def stepAdminFirstName(message: Message, state: FSMContext):
    await state.update_data(admin_id=message.text)
    await message.delete()
    data = await state.get_data()
    await state.set_state(CreatingAdminSteps.GET_FIRST_NAME)
    await data['previousMessage'].edit_text('Введите имя администратора', reply_markup=gеtGoSettingsAdminKeykeyboard())


@router.message(CreatingAdminSteps.GET_FIRST_NAME, F.text)
async def stepAdminLastName(message: Message, state: FSMContext):
    await state.update_data(admin_first_name=message.text)
    await message.delete()
    data = await state.get_data()
    await state.set_state(CreatingAdminSteps.GET_LAST_NAME)
    await data['previousMessage'].edit_text('Введите фамилию администратора', reply_markup=gеtGoSettingsAdminKeykeyboard())


@router.message(CreatingAdminSteps.GET_LAST_NAME, F.text)
async def stepAdminGetPhone(message: Message, state: FSMContext):
    await state.update_data(admin_last_name=message.text)
    await message.delete()
    data = await state.get_data()
    await state.set_state(CreatingAdminSteps.GET_PHONE)
    await data['previousMessage'].edit_text('Введите номер телефона администратора', reply_markup=gеtGoSettingsAdminKeykeyboard())


@router.message(CreatingAdminSteps.GET_PHONE, F.text)
async def stepAdminGetPhone(message: Message, state: FSMContext):
    await state.update_data(admin_phone=message.text)
    await message.delete()
    data = await state.get_data()
    await state.set_state(CreatingAdminSteps.GET_PHOTO)
    await data['previousMessage'].edit_text('Отправьте фотографию администратора', reply_markup=gеtGoSettingsAdminKeykeyboard())


@router.message(CreatingAdminSteps.GET_PHOTO, F.photo)
async def stepAdminGetPhoto(message: Message, state: FSMContext):
    # нужно сделать сохрание фото
    await state.update_data(admin_photo_id=message.photo[-1].file_id)
    await message.delete()
    data = await state.get_data()
    await state.set_state(CreatingAdminSteps.GET_PASSPORT)
    await data['previousMessage'].edit_text('Отправьте паспорт администратора', reply_markup=gеtGoSettingsAdminKeykeyboard())


@router.message(CreatingAdminSteps.GET_PASSPORT, F.text)
async def stepAdminGetPassport(message: Message, state: FSMContext, request: Request):
    await state.update_data(admin_passport=message.text)
    await message.delete()
    data = await state.get_data()
    await state.set_state(CreatingAdminSteps.GET_POINT)
    await data['previousMessage'].edit_text('Отправьте адрес пункта, в котором работает администратор', reply_markup=gеtGoSettingsAdminKeykeyboard())
    mess = await data['previousMessage'].answer(getAllPoints(await request.getAllPoints()))
    await state.update_data(messagesToDelete=[mess])


@router.message(CreatingAdminSteps.GET_POINT, F.text)
async def stepAdminGetDistrict(message: Message, state: FSMContext, request: Request, bot: Bot):
    await state.update_data(admin_point=message.text)
    await message.delete()
    await state.set_state(CreatingAdminSteps.DONE)
    adminData = await state.get_data()
    for mess in adminData['messagesToDelete']:
        await mess.delete()
    await request.insertNewAdmin(data=adminData)
    chat_id = adminData['previousMessage'].chat.id
    await bot.send_photo(chat_id=chat_id, caption=getAllAdminCardData(adminData), photo=adminData['admin_photo_id'])
    await adminData['previousMessage'].edit_text('Анкета администратор создана!', reply_markup=gеtGoSettingsAdminKeykeyboard())
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