from pydantic import BaseModel


class AddItem(BaseModel):
    name: str


class CreateUser(BaseModel):
    user_id: int
    screen_name: str
    full_name: str


class DeleteItem(BaseModel):
    item_name: str


class SaveHistory(BaseModel):
    user_id: int
    item_name: str
    alteration: int
