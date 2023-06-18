from typing import Callable, Dict, Any, Awaitable
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message

from async_http_api.loader import api_wrapper


class CreateUserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        await api_wrapper.create_user(event.from_user.id, event.from_user.username, event.from_user.full_name)
        await handler(event, data)
