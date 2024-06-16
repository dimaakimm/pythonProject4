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
    GET_RAW_CAT_FOOD = State()
    GET_DRY_CAT_FOOD = State()
    GET_RAW_DOG_FOOD = State()
    GET_DRY_DOG_FOOD = State()
    GET_PHOTO = State()


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


class TakeFoodSteps(StatesGroup):
    GET_POINT_ADDRESS = State()
    GET_RAW_CAT_FOOD = State()
    GET_DRY_CAT_FOOD = State()
    GET_RAW_DOG_FOOD = State()
    GET_DRY_DOG_FOOD = State()
    GET_PHOTO = State()


class AddFoodToPointSteps(StatesGroup):
    START = State()
    GET_FOOD_TYPE = State()
    GET_VOLUME = State()
    DONE = State()


class DeliveryFoodSteps(StatesGroup):
    GET_RAW_CAT_FOOD = State()
    GET_DRY_CAT_FOOD = State()
    GET_RAW_DOG_FOOD = State()
    GET_DRY_DOG_FOOD = State()
    GET_COMMENT = State()
    GET_PHOTO = State()
    DONE = State()


class FeedAnimalSteps(StatesGroup):
    START = State()
    GET_RAW_CAT_FOOD = State()
    GET_DRY_CAT_FOOD = State()
    GET_RAW_DOG_FOOD = State()
    GET_DRY_DOG_FOOD = State()
    GET_COMMENT = State()
    GET_PHOTO = State()
    DONE = State()


class EditPointsSteps(StatesGroup):
    GET_POINT_DISTRICT = State()
    GET_POINT_ADDRESS = State()