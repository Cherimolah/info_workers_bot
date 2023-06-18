import json
from json.decoder import JSONDecodeError
from abc import ABC

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class PayloadFilter(BaseFilter, ABC):

    def __init__(self, payload: str):
        self.payload = payload

    async def __call__(self, query: CallbackQuery):
        try:
            data = json.loads(query.data)
        except JSONDecodeError:
            return False
        if self.payload not in data:
            return False
        return {self.payload: data[self.payload]}


class NumericRule(BaseFilter, ABC):

    def __init__(self, min_value: int = None):
        self.min_value = min_value

    async def __call__(self, m: Message):
        try:
            num = int(m.text)
        except ValueError:
            await m.answer("Введите число")
            return False
        if self.min_value and num < self.min_value:
            await m.answer(f"Число должно быть больше {self.min_value}")
            return False
        return {"number": num}
