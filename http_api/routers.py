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