from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo
def get_inline_start_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='О нас', callback_data='aboutUs')
    keyboard_builder.button(text='Посмотреть питомцев', callback_data='choosePet')
    keyboard_builder.button(text='Сделать пожертвование', callback_data='donate')
    keyboard_builder.button(text='Отправить геолокацию', callback_data='sendGeo')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)
def get_inline_choose_pet_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Задать вопрос', callback_data='askAboutPet')
    keyboard_builder.button(text='Следующий', callback_data='nextPet')
    keyboard_builder.button(text='Назад', callback_data='goMenuFromPets')
    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(one_time_keyboard=True)
def gеt_go_menu_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def gеt_go_menu_location_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Заявка', web_app=WebAppInfo(url='https://dimaakimm.github.io/telegramweb/'))
    keyboard_builder.button(text='Сайт', web_app=WebAppInfo(url='https://urbananimal.ru/nakormi'))
    keyboard_builder.button(text='В меню', callback_data='goMenuLocation')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)