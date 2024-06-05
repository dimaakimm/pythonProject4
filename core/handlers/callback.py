from aiogram.types import Message
import random
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from core.keyboards.inline import get_inline_choose_pet_keyboard, get_inline_start_keyboard, get_inline_info_keyboard
from core.parser.parser import Client
parser = Client()
parser.parse()
pets = parser.getPets
class user_status(StatesGroup):
    aboutUs = State()
    choosePet = State()
async def select_category(call: CallbackQuery, bot: Bot):
    answer = str(call.data)
    if answer=="aboutUs":
        await call.message.delete()
        await call.message.answer_photo(photo='https://s6.planeta.ru/i/2fa3ae/1603273696738_renamed.jpg',
                                        caption="Типо мы проект Накорми. а кого кормить хз", reply_markup=get_inline_info_keyboard())
    elif answer == "choosePet":
        await call.message.delete()
        await call.message.answer("Вы выбрали просмотр котиков!")
        await next_pet(call, bot)
    elif answer == "nextPet":
        await call.message.edit_reply_markup()
        await next_pet(call, bot)
    elif answer == "goMenu":
        await call.message.delete()
        await call.message.answer(f'<b>Снова привет!\nМожешь ознакомиться с нашим проектом)</b>', reply_markup=get_inline_start_keyboard())
    elif answer == "goMenuFromPets":
        await call.message.edit_reply_markup()
        await call.message.answer(
            f'<b>Снова привет, {call.message.from_user.first_name}!\nМожешь ознакомиться с нашим проектом)</b>',
            reply_markup=get_inline_start_keyboard())


async def next_pet(call: CallbackQuery, bot: Bot):
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