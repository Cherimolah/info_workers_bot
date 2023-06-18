from aiogram.fsm.state import StatesGroup, State


class TakeFromStorage(StatesGroup):
    choose_item = State()
    count = State()


class PutToStorage(StatesGroup):
    choose_item = State()
    count = State()


class NewItem(StatesGroup):
    choose_name = State()


class DeleteItem(StatesGroup):
    choose_name = State()


class HistoryItem(StatesGroup):
    choose_name = State()
