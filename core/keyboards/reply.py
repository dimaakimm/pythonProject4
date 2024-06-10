from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo
def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Button 1', web_app=WebAppInfo(url='https://dimaakimm.github.io/telegramweb/'))
    keyboard_builder.button(text='Button 2')
    keyboard_builder.button(text='Button 3')
    keyboard_builder.button(text='Send geolocation', request_location=True)
    keyboard_builder.button(text='Send phone contact', request_contact=True)
    keyboard_builder.button(text='Send poll', request_poll=KeyboardButtonPollType())
    keyboard_builder.adjust(3, 2, 1)
    return keyboard_builder.as_markup(resize_keyboard = True, one_time_keyboard = True, input_field_placeholder="Click a btn!")
