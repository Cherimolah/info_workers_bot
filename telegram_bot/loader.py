from aiogram import Bot, Dispatcher

from telegram_bot.config import BOT_TOKEN
from telegram_bot.middlewares import CreateUserMiddleware

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.message.middleware(CreateUserMiddleware())
