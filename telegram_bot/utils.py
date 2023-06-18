import datetime
import json

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from async_http_api.loader import api_wrapper


DATE_FORMAT = "%d.%m.%Y %H:%M:%S"


async def send_pagination(event: Message | CallbackQuery, data, reply, payload, page: int = 1,
                          main_menu_button=False):
    keyboard = InlineKeyboardBuilder()
    if page > 1:
        keyboard.add(InlineKeyboardButton(text="<-", callback_data=json.dumps({payload: page - 1})))
    if page < data.count_pages:
        keyboard.add(InlineKeyboardButton(text="->", callback_data=json.dumps({payload: page + 1})))
    if main_menu_button:
        keyboard.row(InlineKeyboardButton(text="Главное меню", callback_data=json.dumps({"start": "start"})))
    if isinstance(event, Message):
        await event.answer(reply, parse_mode="Markdown", reply_markup=keyboard.as_markup())
    else:
        await event.message.edit_text(reply, parse_mode="Markdown", reply_markup=keyboard.as_markup())


async def send_list_items(event: Message | CallbackQuery, payload, page: int = 1):
    data = await api_wrapper.get_all_items(page)
    reply = f"*Спсиок всех расходников и их количество*\n" \
            f"Страница {data.current_page}/{data.count_pages}\n\n"
    for i, item in enumerate(data.items):
        reply = f"{reply}{i + 1}. {item.item_name} - {item.count}\n"
    await send_pagination(event, data, reply, payload, page)


async def send_history(event: Message | CallbackQuery, item_name, payload, page: int = 1):
    data = await api_wrapper.get_history_by_item_name(item_name, page)
    reply = f"*История расходника {item_name}*\n" \
            f"Страница {data.current_page}/{data.count_pages}\n\n"
    if not data.history:
        return await event.answer("Для данного расходника нет изменений")
    for i, item in enumerate(data.history):
        reply = f"{reply}{i+1}. [{item.user_id}](tg://user?user_id={item.user_id}) " \
                f"{'взял' if item.alteration < 0 else 'положил'} в " \
                f"{datetime.datetime.fromtimestamp(item.created_at).strftime(DATE_FORMAT)}\n"
    await send_pagination(event, data, reply, payload, page, True)
