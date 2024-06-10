import random
import json
from aiogram import Bot, F, Router
from aiogram.types import Message
from core.keyboards.inline import get_inline_choose_pet_keyboard, get_inline_start_keyboard, gеt_go_menu_keyboard, gеt_go_menu_location_keyboard
from core.keyboards.reply import reply_keyboard, get_reply_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from core.parser.parser import Client
from core.settings import settings
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType

bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
router = Router()
parser = Client()
parser.parse()
pets = parser.getPets
last_message = None
last_location = None
last_location_send = None
class user_status(StatesGroup):
    aboutUs = State()
    choosePet = State()
    sendLocation = State()

@router.shutdown()
async def stopBot():
    await bot.send_message(settings.bots.admin_id, text='Bot is off!')

@router.startup()
async def startBot():
    await bot.send_message(settings.bots.admin_id, text='Bot is on!')

@router.message(Command(commands=['help']))
async def cmdStart(message: Message):
    await message.answer(f'<b>Привет, {message.from_user.first_name}!\nМожешь ознакомиться с нашим проектом)</b>)', reply_markup=get_reply_keyboard())
    await bot.send_message(chat_id=5474812547, text='334', reply_markup=get_inline_start_keyboard())

@router.message(Command(commands=['start', 'run']))
async def cmdStart(message: Message):
    await message.answer(f'<b>Привет, {message.from_user.first_name}!\nМожешь ознакомиться с нашим проектом)</b>)', reply_markup=get_inline_start_keyboard())

@router.callback_query(F.data=="aboutUs")
async def aboutUs(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer_photo(photo='https://s6.planeta.ru/i/2fa3ae/1603273696738_renamed.jpg',
                                    caption="Типо мы проект Накорми. а кого кормить хз",
                                    reply_markup=gеt_go_menu_keyboard())

@router.callback_query(F.data=="choosePet")
async def choosePet(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Вы выбрали просмотр котиков!")
    await next_pet(call)

@router.callback_query(F.data=="donate")
async def donate(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Вы выбрали просмотр котиков!")
    await next_pet(call)

@router.callback_query(F.data=="sendGeo")
async def askGeo(call: CallbackQuery, state: FSMContext):
    await state.set_state(user_status.sendLocation)
    await call.message.edit_reply_markup()
    await call.message.delete()
    global last_location_send
    last_location_send = await call.message.answer("Отправьте нам свою геолокацию!", reply_markup=gеt_go_menu_location_keyboard())

@router.message(F.location, user_status.sendLocation)
async def determineCityByGeo(message: Message, state: FSMContext):
    global last_message, last_location, last_location_send
    if hasattr(last_location, 'message_id'):
        await bot.delete_message(message.chat.id, last_location.message_id)
    if hasattr(last_message, 'message_id'):
        await bot.delete_message(message.chat.id, last_message.message_id)
    if hasattr(last_location_send, 'message_id'):
        await bot.delete_message(message.chat.id, last_location_send.message_id)
        last_location_send = None
    last_message = await message.answer('Вы отправили свою геолокацию! Можете отправить ее снова или вернуть в начальное меню\r\a'
                         f'{message.location.latitude}\r\n{message.location.longitude}', reply_markup=gеt_go_menu_location_keyboard())
    last_location = message


@router.callback_query(F.data=="nextPet")
async def nextPet(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await next_pet(call)

@router.callback_query(F.data=="goMenu")
async def goMenu(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(f'<b>Снова привет!\nМожешь ознакомиться с нашим проектом)</b>',
                              reply_markup=get_inline_start_keyboard())
@router.callback_query(F.data=="goMenuLocation")
async def goMenu(call: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    global last_location_send, last_message, last_location
    if hasattr(last_location_send, 'message_id'):
        await bot.delete_message(call.message.chat.id, last_location_send.message_id)
    if last_message:
        await call.message.edit_reply_markup()
    await call.message.answer(f'<b>Снова привет!\nМожешь ознакомиться с нашим проектом)</b>',
                              reply_markup=get_inline_start_keyboard())
    last_message = None
    last_location = None
    last_location_send = None

@router.callback_query(F.data=="goMenuFromPets")
async def goMenuFromPets(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(
        f'<b>Снова привет, {call.message.from_user.first_name}!\nМожешь ознакомиться с нашим проектом)</b>',
        reply_markup=get_inline_start_keyboard())

@router.message(F.content_type == ContentType.WEB_APP_DATA)
async def getWebAppData(message: Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(f'Name: {res["forename"]}\nSurname: {res["surname"]}\nEmail: {res["email"]}\nPhone number: {res["phonenumber"]}')


async def next_pet(call: CallbackQuery):
    i = random.randint(0,29)
    pet = pets[i]
    name = pet.getNamePet
    age = pet.getAgePet
    sex = pet.getSexPet
    info = pet.getInformationPet
    url = pet.getUrlPet
    if len(info)>696:
        info = info[ : 696] + "..."
    await call.message.answer_photo(photo=url, caption=f'Name:  <a href=\'{url}\'><b>{name}</b></a>\nAge: <b>{age}</b>\nSex: <b>{sex}</b>\n{info[0:700]}', reply_markup=get_inline_choose_pet_keyboard())

@router.message()
async def unknownMessage(message: Message):
    await message.answer("Извините, я вас не понял..")