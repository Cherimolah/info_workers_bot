import datetime
import json

from gino import Gino
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

db = Gino()


class Item(db.Model):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    count = Column(Integer, default=0)

    def json(self):
        return {"id": self.id, "name": self.name, "count": self.count}


class User(db.Model):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    screen_name = Column(String)
    full_name = Column(String)

    def __init__(self, user_id, screen_name, full_name):
        self.user_id = user_id
        self.screen_name = screen_name
        self.full_name = full_name

    def json(self):
        return {"user_id": self.user_id, "screen_name": self.screen_name, "full_name": self.full_name}


class History(db.Model):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id, ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey(Item.id, ondelete="CASCADE"))
    alteration = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)

