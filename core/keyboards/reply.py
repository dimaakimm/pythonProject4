from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text = 'Row1Col1'
        ),
        KeyboardButton(
            text = 'Row1Col2'
        ),
        KeyboardButton(
            text = 'Row1Col3'
        )
    ],
    [
        KeyboardButton(
            text = 'Row2Col1'
        ),
        KeyboardButton(
            text = 'Row2Col2'
        ),
        KeyboardButton(
            text = 'Row2Col3'
        ),
        KeyboardButton(
            text = 'Row2Col4'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Choose btn", selective=True)




def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Button 1')
    keyboard_builder.button(text='Button 2')
    keyboard_builder.button(text='Button 3')
    keyboard_builder.button(text='Send geolocation', request_location=True)
    keyboard_builder.button(text='Send phone contact', request_contact=True)
    keyboard_builder.button(text='Send poll', request_poll=KeyboardButtonPollType())
    keyboard_builder.adjust(3, 2, 1)
    return keyboard_builder.as_markup(resize_keyboard = True, one_time_keyboard = True, input_field_placeholder="Click a btn!")
