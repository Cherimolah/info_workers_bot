import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String, DateTime

from loader import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, unique=True)
    count = db.Column(Integer, default=0)

    def __init__(self, name, count=0):
        self.name = name
        self.count = count


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(Integer, primary_key=True)
    screen_name = db.Column(String)
    full_name = db.Column(String)

    def __init__(self, user_id, screen_name, full_name):
        self.user_id = user_id
        self.screen_name = screen_name
        self.full_name = full_name


class History(db.Model):
    __tablename__ = "history"

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey(User.user_id, ondelete="CASCADE"))
    item_id = db.Column(Integer, ForeignKey(Item.id, ondelete="CASCADE"))
    alteration = db.Column(Integer)
    created_at = db.Column(DateTime, default=datetime.datetime.now)

    def __init__(self, user_id, item_id, alteration, created_at=None):
        self.user_id = user_id
        self.item_id = item_id
        self.alteration = alteration
        self.created_at = created_at or datetime.datetime.now()


with app.app_context():
    db.create_all()
