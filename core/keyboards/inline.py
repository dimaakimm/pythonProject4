from aiogram.utils.keyboard import InlineKeyboardBuilder

def getInlineStartAdminKeyBoard():
    keyboard_builder = InlineKeyboardBuilder()
    # keyboard_builder.button(text='Получить данные заявок на кор', callback_data='getAllRequest')
    keyboard_builder.button(text='Настройки пользователей', callback_data='getUsersSettings')
    keyboard_builder.button(text='Настройки пункта', callback_data='getPointSettings')
    keyboard_builder.button(text='Работа с волонтерами', callback_data='getVolunteerWork')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def getInlineUserSettingsKeyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Добавить нового администратора', callback_data='insertAdmin')
    keyboard_builder.button(text='Удалить администратора', callback_data='deleteAdmin')
    keyboard_builder.button(text='Добавить нового волонтера', callback_data='insertVolunteer')
    keyboard_builder.button(text='Удалить волонтера', callback_data='deleteVolunteer')
    keyboard_builder.button(text='Изменить данные волонтера', callback_data='updateVolunteer')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(one_time_keyboard=True)



def gеt_accept_keyboard(fromId, toId, volume):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Согласиться', callback_data=f'accept{fromId}-{toId}-{volume}')
    keyboard_builder.button(text='Отказать', callback_data=f'decline{fromId}-{toId}')
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def gеt_pet_keyboard(pet_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Удалить питомца', callback_data=f'petDelete{pet_id}')
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def gеtStartKeyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Войти как админ', callback_data=f'loginAsAdmin')
    keyboard_builder.button(text='Войти как волонтер', callback_data='loginAsVolunteer')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def gеt_volunteer_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Передать корм', callback_data=f'volGiveFood')
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)
def getInlineStartVolunteerKeyBoard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Показать профиль', callback_data='showProfile')
    keyboard_builder.button(text='Добавить питомца', callback_data='addPet')
    keyboard_builder.button(text='Показать питомцев', callback_data='showPets')
    keyboard_builder.button(text='Найти волонтера', callback_data='findProfile')

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineKeyboardPet(allRequests):
    keyboard_builder = InlineKeyboardBuilder()
    for record in allRequests:
        keyboard_builder.button(text=record['name'], callback_data=f"showAPet{record['id']}")
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)
def gеt_go_menu_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)