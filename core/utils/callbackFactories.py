from aiogram.filters.callback_data import CallbackData


class AddFoodToPoint(CallbackData, prefix="addFoodToPoint"):
    foodType: str
