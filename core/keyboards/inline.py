from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_inline_start_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='О нас', callback_data='aboutUs')
    keyboard_builder.button(text='Посмотреть питомцев', callback_data='choosePet')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)
def get_inline_choose_pet_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Задать вопрос', callback_data='askAboutPet')
    keyboard_builder.button(text='Следующий', callback_data='nextPet')
    keyboard_builder.button(text='Назад', callback_data='goMenuFromPets')
    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(one_time_keyboard=True)
def get_inline_info_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)