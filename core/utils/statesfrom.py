from aiogram.fsm.state import StatesGroup, State


class VolStepsFormAddPet(StatesGroup):
    GET_NAME = State()
    GET_PHOTO = State()
    GET_INFO = State()
    GET_STERILIZED = State()
    GET_DISTRICT = State()
    GET_CONFIRM = State()