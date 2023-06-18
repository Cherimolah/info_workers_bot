from typing import List

from msgspec import Struct


class History(Struct):
    user_id: int
    user_name: str
    item_name: str
    alteration: int
    created_at: int


class HistoryByItem(Struct):
    count_pages: int
    current_page: int
    history: List[History]


class Item(Struct):
    item_name: str
    count: int


class AllItems(Struct):
    count_pages: int
    current_page: int
    items: List[Item]


class ExistItem(Struct):
    exists: bool


class Users(Struct):
    user_id: int
    user_name: str


class AllUsers(Struct):
    user_ids: List[Users]


class CountItem(Struct):
    count: int
