from aiogram.utils.keyboard import InlineKeyboardBuilder

def gеt_pet_keyboard(pet_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Удалить питомца', callback_data=f'petDelete{pet_id}')
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)
def getInlineStartKeyBoard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Получить данные заявок на корм', callback_data='getAllRequest')
    keyboard_builder.button(text='Показать профиль', callback_data='showProfile')
    keyboard_builder.button(text='Добавить питомца', callback_data='addPet')
    keyboard_builder.button(text='Показать питомцев', callback_data='showPets')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineKeyboardPet(allRequests):
    keyboard_builder = InlineKeyboardBuilder()
    for record in allRequests:
        keyboard_builder.button(text=record['name'], callback_data=f"showAPet{record['id']}")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)
def gеt_go_menu_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)