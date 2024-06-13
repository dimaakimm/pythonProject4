from aiogram.fsm.state import StatesGroup, State


class VolStepsFormAddPet(StatesGroup):
    GET_NAME = State()
    GET_PHOTO = State()
    GET_INFO = State()
    GET_STERILIZED = State()
    GET_DISTRICT = State()
    GET_CONFIRM = State()

class VolFriends(StatesGroup):
    GET_PROFILE = State()
    GET_PHOTO = State()
    GIVE_FOOD = State()


class CreatingAdminSteps(StatesGroup):
    GET_ID = State()
    GET_FIRST_NAME = State()
    GET_LAST_NAME = State()
    GET_PHONE = State()
    GET_PHOTO = State()
    GET_PASSPORT = State()
    GET_POINT = State()
    DONE = State()


class CreatingVolunteerSteps(StatesGroup):
    GET_ID = State()
    GET_FIRST_NAME = State()
    GET_LAST_NAME = State()
    GET_PHONE = State()
    GET_EMAIL = State()
    GET_PASSPORT = State()
    GET_PHOTO_ID = State()
    GET_BALANCE = State()
    DONE = State()

class DeletingVolunteerSteps(StatesGroup):
   GET_ID = State()

class DeletingAdminSteps(StatesGroup):
   GET_ID = State()