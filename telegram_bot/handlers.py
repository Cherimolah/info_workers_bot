from aiogram.types import Message

from telegram_bot.loader import dp


@dp.message_handler(commands="start")
async def start(m: Message):
    await m.answer("Привет! Это сервис об информировании остатков расходников")
