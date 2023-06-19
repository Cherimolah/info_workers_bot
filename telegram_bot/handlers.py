from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import CommandStart, Text
from aiogram.fsm.context import FSMContext

from telegram_bot.loader import dp, bot
from telegram_bot.utils import send_list_items, send_history
from telegram_bot.filters import PayloadFilter, NumericRule
from telegram_bot.states import *
import telegram_bot.keyboards as keyboards
from async_http_api.loader import api_wrapper


@dp.message(CommandStart())
@dp.callback_query(PayloadFilter("start"))
async def start(m: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if isinstance(m, CallbackQuery):
        await m.message.delete()
    await bot.send_message(m.from_user.id,
                           "Добро пожаловать в наш Сервис информирования! "
                           "Мы рады приветствовать вас здесь и готовы помочь вам быть в курсе остатков расходников. "
                           "Бот предоставляет удобный доступ к информации о наличии расходных материалов. "
                           "Надеемся, что наш сервис будет полезным для вас и сделает вашу работу более "
                           "комфортной и эффективной.", reply_markup=keyboards.main_menu)


@dp.message(Text("Список расходников"))
@dp.callback_query(PayloadFilter("item_page"))
async def hello(m: Message, item_page: int = 1):
    await send_list_items(m, "item_page", item_page)


@dp.message(Text("Взять со склада"))
async def take_from_storage(m: Message, state: FSMContext):
    await state.set_state(TakeFromStorage.choose_item)
    await m.answer("Напишите название расходника, которого хотите взять со склада", reply_markup=ReplyKeyboardRemove())


@dp.message(TakeFromStorage.choose_item)
async def choose_name_to_take(m: Message, state: FSMContext):
    if not (await api_wrapper.check_item_name(m.text.lower())).exists:
        return await m.answer("Введено неверное имя расходника!")
    if (await api_wrapper.get_count_item_name(m.text.lower())).count == 0:
        return await m.answer("Расходника на складе нет!")
    await state.update_data(item_name=m.text.lower())
    await state.set_state(TakeFromStorage.count)
    await m.answer("Укажите количество расходника")


@dp.message(TakeFromStorage.count, NumericRule(1))
async def set_count_to_take(m: Message, state: FSMContext, number: int):
    data = await state.get_data()
    count = (await api_wrapper.get_count_item_name(data['item_name'].lower())).count
    if count - number < 0:
        return await m.answer("Количество предмета не может быть меньше 0\n"
                       f"Сейчас на складе: {count}")
    await api_wrapper.save_history(m.from_user.id, data['item_name'], -number)
    await state.clear()
    await m.answer(f"Вы успешно взяли со склада {number}  шт. расходника {data['item_name']}",
                   reply_markup=keyboards.main_menu)
    user_ids = (await api_wrapper.get_all_user_ids()).user_ids
    chat = await bot.get_chat(m.from_user.id)
    for user in user_ids:
        await bot.send_message(user.user_id, f"Пользователь [{chat.full_name}](tg://user?user_id={chat.id}) "
                                     f"взял расходник {data['item_name']} в количестве {number} шт.\n"
                                             f"Осталось: {count - number}",
                               parse_mode="Markdown")


@dp.message(Text("Положить на склад"))
async def put_from_storage(m: Message, state: FSMContext):
    await state.set_state(PutToStorage.choose_item)
    await m.answer("Напишите название расходника, который хотите положить на склад",
                   reply_markup=ReplyKeyboardRemove())


@dp.message(PutToStorage.choose_item)
async def choose_name_to_put(m: Message, state: FSMContext):
    if not (await api_wrapper.check_item_name(m.text.lower())).exists:
        return await m.answer("Введено неверное имя расходника!")
    await state.update_data(item_name=m.text.lower())
    await state.set_state(PutToStorage.count)
    await m.answer("Укажите количество расходника")


@dp.message(PutToStorage.count, NumericRule(1))
async def set_count_to_put(m: Message, state: FSMContext, number: int):
    data = await state.get_data()
    await api_wrapper.save_history(m.from_user.id, data['item_name'], number)
    await state.clear()
    await m.answer(f"Вы успешно положили на склад {number} шт. расходника {data['item_name']}",
                   reply_markup=keyboards.main_menu)
    count = (await api_wrapper.get_count_item_name(data['item_name'].lower())).count
    user_ids = (await api_wrapper.get_all_user_ids()).user_ids
    chat = await bot.get_chat(m.from_user.id)
    for user in user_ids:
        await bot.send_message(user.user_id, f"Пользователь [{chat.full_name}](tg://user?user_id={chat.id}) "
                                     f"положил на склад расходник {data['item_name']} в количестве {number} шт.\n"
                                             f"Осталось: {count} шт.",
                               parse_mode="Markdown")


@dp.message(Text("Новый расходник"))
async def new_item(m: Message, state: FSMContext):
    await state.set_state(NewItem.choose_name)
    await m.answer("Напишите название нового расходника", reply_markup=ReplyKeyboardRemove())


@dp.message(NewItem.choose_name)
async def chose_new_item_name(m: Message, state: FSMContext):
    if (await api_wrapper.check_item_name(m.text.lower())).exists:
        return await m.answer(f"Расходник {m.text} уже существует!")
    await api_wrapper.add_item(m.text.lower())
    await state.clear()
    await m.answer(f"Расходник {m.text} успешно добавлен", reply_markup=keyboards.main_menu)


@dp.message(Text("Удалить расходник"))
async def new_item(m: Message, state: FSMContext):
    await state.set_state(DeleteItem.choose_name)
    await m.answer("Напишите название расходника, который хотите удалить\n\n"
                   "*❗️ Вместе с этим удалится вся история изменений этого расходника*",
                   reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")


@dp.message(DeleteItem.choose_name)
async def chose_new_item_name(m: Message, state: FSMContext):
    if not (await api_wrapper.check_item_name(m.text.lower())).exists:
        return await m.answer(f"Расходника {m.text} не существует!")
    await api_wrapper.delete_item(m.text.lower())
    await state.clear()
    await m.answer(f"Расходник {m.text} успешно удалён", reply_markup=keyboards.main_menu)


@dp.message(Text("История изменений расходника"))
async def history_item(m: Message, state: FSMContext):
    await state.set_state(HistoryItem.choose_name)
    await m.answer("Напишите название расходника по которому хотите посмотреть историю",
                   reply_markup=ReplyKeyboardRemove())


@dp.message(HistoryItem.choose_name)
@dp.callback_query(PayloadFilter("history_page"))
async def choose_history_item_name(m: Message | CallbackQuery, state: FSMContext, history_page: int = 1):
    if isinstance(m, Message):
        await state.update_data(item_name=m.text.lower())
    item_name = (await state.get_data())['item_name']
    if not (await api_wrapper.check_item_name(item_name)).exists:
        return await m.answer(f"Расходника {m.text} не существует!")
    await send_history(m, item_name, "history_page", history_page)
