import asyncio

import uvicorn

from async_http_api.routers import app
from telegram_bot.handlers import dp, bot
from async_http_api.models import db
from async_http_api.config import USER, PASSWORD, HOST, DATABASE


@app.on_event("startup")
async def start_up():
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
    await db.set_bind(f"postgresql://{USER}:{PASSWORD}@{HOST}/{DATABASE}")
    await db.gino.create_all()


if __name__ == '__main__':
    uvicorn.run(app, loop="asyncio", port=8001)
