import json

from flask import request
from sqlalchemy import update, delete, select, func

from loader import app
from models import db, Item, User, History


@app.get("/")
def index():
    return "<p>Hello World!</p>"


@app.post("/add_item")
def add_item():
    name = request.json.get("name")
    item = Item(name)
    db.session.add(item)
    db.commit()
    return json.dumps({"response": "ok"})


@app.post("/create_user")
def create_user():
    user_id: int = request.json.get('user_id')
    screen_name = request.json.get('screen_name')
    full_name = request.json.get("full_name")
    user = User.query.get(user_id)
    if not user:
        user = User(user_id, screen_name, full_name)
        db.session.add(user)
        db.session.commit()
    else:
        db.session.execute(update(User).where(User.user_id == user_id).values(screen_name=screen_name,
                                                                              full_name=full_name))
        db.session.commit()
    return f"User has ben updated"


@app.delete("/delete_item")
def delete_item():
    item_name: str = request.json.get("item_name")
    db.session.execute(delete(Item).where(Item.name == item_name))
    db.session.commit()
    return "Item deleted"


@app.post("/save_history")
def save_history():
    user_id = request.json.get("user_id")
    item_name: str = request.json.get("item_nme")
    alteration: int = request.json.get("alteration")
    item_id = db.session.execute(
        select(Item.id).where(Item.name == item_name)
    ).scalar()
    history = History(user_id, item_id, alteration)
    db.session.add(history)
    db.session.commit()
    return "History saved"


@app.get("/get_history_by_item_name")
def get_history_by_item_id():
    item_name: str = request.json.get("item_name")
    item_id: int = db.session.execute(
        select(Item.id).where(Item.name == item_name)
    ).scalar()
    page = int(request.json.get("page", 1))
    response = db.session.execute(
        select(History, Item.name).where(History.item_id == item_id).offset((page - 1) * 10).limit(10)
        .join(Item)
    ).all()
    count_records = db.session.execute(
        select(func.count(History.item_id)).where(History.item_id == item_id)
    ).scalar()
    count_pages = int(count_records / 10) if count_records % 10 == 0 else int(count_records // 10 + 1)
    return {"count_pages": count_pages,
            "history": [{
                "user_id": story.user_id,
                "item_name": item_name,
                "alteration": story.alteration,
                "created_at": story.created_at
            } for story, item_name in response]}


@app.get("/get_all_items")
def get_all_items():
    page = request.json.get('page', 1)
    response = db.session.execute(
        select(History, Item.name).offset((page - 1) * 10).limit(10).join(Item)
    ).all()
    count_records = db.session.execute(
        select(func.count(History.item_id))
    ).scalar()
    count_pages = int(count_records / 10) if count_records % 10 == 0 else int(count_records // 10 + 1)
    return {
        "count_pages": count_pages,
        "history": [{
            "user_id": story.user_id,
            "item_name": item_name,
            "alteration": story.alteration,
            "created_at": story.created_at
        } for story, item_name in response]}
