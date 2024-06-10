from aiogram import Bot, F, Router
from aiogram.types import Message
from core.keyboards.inline import get_inline_choose_pet_keyboard, get_inline_start_keyboard, gеt_go_menu_keyboard, gеt_go_menu_location_keyboard
from core.keyboards.reply import get_reply_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from core.settings import settings
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType

bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
router = Router()
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

@router.message(Command(commands=['start', 'run'])) #check the role of a user
async def cmdStart(message: Message):
    await message.answer(f'<b>Привет, {message.from_user.first_name}!\nМожешь ознакомиться с нашим проектом)</b>)', reply_markup=get_inline_start_keyboard())

@router.callback_query(F.data=="aboutUs")
async def aboutUs(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer_photo(photo='https://s6.planeta.ru/i/2fa3ae/1603273696738_renamed.jpg',
                                    caption="Типо мы проект Накорми. а кого кормить хз",
                                    reply_markup=gеt_go_menu_keyboard())

def getAllRequestsMessage(allRequests):
    message = "ЗАЯВКИ:\n"
    message += "-------------------------------------------\n"
    for record in allRequests:
        message += f"name: {record['name']}\nsurname: {record['surname']}\nemail: {record['email']}\nphone: {record['phone']}\n"
        message += "-------------------------------------------\n"
    return message

@router.message()
async def unknownMessage(message: Message):
    await message.answer("Извините, я вас не понял..")