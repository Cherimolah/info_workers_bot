from aiogram.types import Message

from loader import dp


@dp.message_handler(commands="start")
async def start_command(m: Message):
    await m.answer("Привет! Это сервис для информирования работников об остатков расходников")
