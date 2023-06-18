from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = kb = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="Список расходников"),
    ], [
        KeyboardButton(text="Взять со склада"),
        KeyboardButton(text="Положить на склад")
    ], [
        KeyboardButton(text="Новый расходник"),
        KeyboardButton(text="Удалить расходник")
    ], [
        KeyboardButton(text="История изменений расходника")
    ]], resize_keyboard=True)
