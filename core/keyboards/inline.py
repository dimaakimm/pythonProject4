from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackFactories import AddFoodToPoint

def getInlineKeyboardVolunteers(allRequests):
    keyboard_builder = InlineKeyboardBuilder()
    for record in allRequests:
        if record['state'] == 'busy':
            continue
        keyboard_builder.button(text=record['forename'] + " - " + record['id'], callback_data=f"orderChoose{record['id']}")
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def getInlineKeyboardPoints(allRequests, id):
    keyboard_builder = InlineKeyboardBuilder()
    for record in allRequests:
        keyboard_builder.button(text=f"{record['address']} - {record['id']}", callback_data=f"orderCreate{id}-{record['id']}")
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getGoAdmiMenyKeyBoard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    return keyboard_builder.as_markup(one_time_keyboard=True)

def getInlineStartAdminKeyBoard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Настройки пользователей', callback_data='getUsersSettings')
    keyboard_builder.button(text='Настройки пункта', callback_data='getPointSettings')
    keyboard_builder.button(text='Работа с волонтерами', callback_data='getVolunteerWork')
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    keyboard_builder.button(text='Выйти из профиля', callback_data='LogOut')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineUserSettingsKeyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Добавить нового администратора', callback_data='insertAdmin')
    keyboard_builder.button(text='Удалить администратора', callback_data='deleteAdmin')
    keyboard_builder.button(text='Добавить нового волонтера', callback_data='insertVolunteer')
    keyboard_builder.button(text='Удалить волонтера', callback_data='deleteVolunteer')
    keyboard_builder.button(text='Изменить данные волонтера', callback_data='updateVolunteer')
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def gеt_accept_keyboard(fromId, toId, volume1, volume2, volume3, volume4):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Согласиться', callback_data=f'accept-{fromId}-{toId}-{volume1}-{volume2}-{volume3}-{volume4}')
    keyboard_builder.button(text='Отказать', callback_data=f'decline-{fromId}-{toId}')
    keyboard_builder.button(text='Назад', callback_data='goVolunteerMenu')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def gеt_pet_keyboard(pet_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Удалить питомца', callback_data=f'petDelete{pet_id}')
    keyboard_builder.button(text='Назад', callback_data='goVolunteerMenu')
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
    keyboard_builder.button(text='Назад', callback_data='goVolunteerMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineStartVolunteerKeyBoard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Показать профиль', callback_data='showProfile')
    keyboard_builder.button(text='Добавить питомца', callback_data='addPet')
    keyboard_builder.button(text='Показать питомцев', callback_data='showPets')
    keyboard_builder.button(text='Найти волонтера', callback_data='findProfile')
    keyboard_builder.button(text='Забрать заказ', callback_data='takeFood')
    keyboard_builder.button(text='Доставить заказ', callback_data='deliveryFood')
    keyboard_builder.button(text='Покормить животных', callback_data='feedAnimals')
    keyboard_builder.button(text='Выйти из профиля', callback_data='LogOut')

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineKeyboardPet(allRequests):
    keyboard_builder = InlineKeyboardBuilder()
    for record in allRequests:
        keyboard_builder.button(text=record['name'], callback_data=f"showAPet{record['id']}")
    keyboard_builder.button(text='Назад', callback_data='goVolunteerMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def gеt_go_menu_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goVolunteerMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def gеtGoSettingsAdminKeykeyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goAdminSettings')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def petCreateSuccesfulKeyBoard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goVolunteerMenu')
    keyboard_builder.button(text='Верно', callback_data='createPetSuccesful')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def getGoAdminMenyKeyBoard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineKeyboardPointsList(allRequests):
    keyboard_builder = InlineKeyboardBuilder()
    for record in allRequests:
        keyboard_builder.button(text=record['address'], callback_data=f"showPointInfo{record['id']}")
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineKeyboardPointInfo():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Добавить корм', callback_data="addFoodToPoint")
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineKeyboardPointFoodType():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Cухой кошачий', callback_data=AddFoodToPoint(foodType="dry_cat_food"))
    keyboard_builder.button(text='Влажный кошачий', callback_data=AddFoodToPoint(foodType="wet_cat_food"))
    keyboard_builder.button(text='Сухой собачий', callback_data=AddFoodToPoint(foodType="dry_dog_food"))
    keyboard_builder.button(text='Влажный собачий', callback_data=AddFoodToPoint(foodType="wet_dog_food"))
    keyboard_builder.button(text='Назад', callback_data='goAdminMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def getInlineKeyboardPointAddAnotherFood():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Добавить ещё корм', callback_data="addFoodToPoint")
    keyboard_builder.button(text='В меню', callback_data='goAdminMenu')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)

def chooseTypeOfFood():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Cухой кошачий', callback_data="dry_cat_food")
    keyboard_builder.button(text='Влажный кошачий', callback_data="raw_cat_food")
    keyboard_builder.button(text='Сухой собачий', callback_data="dry_dog_food")
    keyboard_builder.button(text='Влажный собачий', callback_data="raw_dog_food")
    keyboard_builder.button(text='Назад', callback_data="goVolunteerMenu")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)

