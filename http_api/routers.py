import json

from flask import request

from loader import app
from db_engine import get_connection


@app.get("/")
def index():
    return "<p>Hello World!</p>"


@app.post("/add_item")
def add_item():
    name = request.args.get("name")
    db, cursor = get_connection()
    cursor.execute("INSERT INTO items(name) VALUES(?)", (name,))
    db.commit()
    return json.dumps({"response": "ok"})


@app.post("/create_user")
def create_user():
    user_id = request.form.get('user_id')
    username = request.form.get('username')
    query = f"INSERT INTO users (user_id, username) VALUES ({user_id}, '{username}')"
    query_db(query)
    return f"Пользователь {username} добавлен с ID {user_id} в базу данных."


@app.delete("/delete_item")
def delete(update, context):
    item_names = context.args
    for item_name in item_names:
        c.execute("SELECT quantity FROM items WHERE name=?", (item_name,))
        item_quantity = c.fetchone()[0]
        new_quantity = item_quantity - 1
        if new_quantity < 0:
            update.message.reply_text(f'Расходник {item_name} закончился.')
        else:
            c.execute("UPDATE items SET quantity=? WHERE name=?", (new_quantity, item_name))
            conn.commit()
            update.message.reply_text(f'Расходник {item_name} взят. Осталось: {new_quantity}.')


@app.post("/save_history")
def save_history():
    user_id = request.args.get("user_id")
    item_id = request.args.get("item_id")
    alteration = int(request.args.get("alteration"))
    history_db.append({"user_id": user_id, "item_id": item_id, "alteration": alteration})
    items_db[item_id]["quantity"] += alteration
    return f"История изменений успешно сохранена. Текущее количество расходника: {items_db[item_id]['quantity']}."


@app.get("/get_history_by_item_id")
def get_history_by_item_id():
    item_id = int(request.args.get("item_id"))
    page = int(request.args.get("page", 1))
    per_page = 10
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    history = [entry for entry in history_db if entry["item_id"] == item_id]
    total_pages = (len(history) - 1) // per_page + 1
    history_page = history[start_index:end_index]
    response = f"История изменений для расходника {items_db[item_id]['name']}:"
    for entry in history_page:
        if entry["alteration"] > 0:
            action = "добавил"
        else:
            action = "удалил"
        response += f"\n- Пользователь {entry['user_id']} {action} {abs(entry['alteration'])} единиц. "
    response += f"\nСтраница {page} из {total_pages}."
    return response


@app.get("/get_all_items")
def get_all_items():
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(page, 10, False)
    if items.items:
        output = ''
        for item in items.items:
            output += f'{item.name}: {item.quantity}\n'
        return output
    else:
        return 'Предметы не найдены'


@app.get("/search_item")
def search_item():
    query = request.args.get('query')
    if not query:
        return {"Ошибка": "No search query provided"}

    items = []
    for item in database:
        if query.lower() in item['name'].lower():
            items.append(item)

    return {"Доступные расходники": items}
