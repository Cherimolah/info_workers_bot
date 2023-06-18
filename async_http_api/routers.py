from fastapi.responses import PlainTextResponse, JSONResponse

from async_http_api.loader import app
from async_http_api.validtors import *
from async_http_api.models import db, Item, User, History


@app.get("/")
async def root():
    return PlainTextResponse("Привет мир!")


@app.post("/add_item")
async def add_item(data: AddItem):
    item = await db.select([Item.id]).where(Item.name == data.name).gino.scalar()
    if item:
        return JSONResponse({"error": f"{item.name} already exists"}, status_code=400)
    await Item.create(name=data.name)
    return JSONResponse({"message": "Item added successfully"})


@app.post("/create_user")
async def create_user(data: CreateUser):
    user = await db.select([*User]).where(User.user_id == data.user_id).gino.first()
    if not user:
        await User.create(user_id=data.user_id, screen_name=data.screen_name, full_name=data.full_name)
    else:
        await (User.update.values(screen_name=data.screen_name, full_name=data.full_name)
               .where(User.user_id == data.user_id).gino.first())
    return JSONResponse({"message": "User data updated successfully"})


@app.delete("/delete_item")
async def delete_item(data: DeleteItem):
    item = await db.select([Item.id]).where(Item.name == data.item_name).gino.scalar()
    if not item:
        return JSONResponse({"error": "Item does not exist"}, status_code=400)
    await Item.delete.where(Item.id == item).gino.status()
    return JSONResponse({"message": "Item deleted successfully"})


@app.post("/save_history")
async def save_history(data: SaveHistory):
    user_id = await db.select([User.user_id]).where(User.user_id == data.user_id).gino.scalar()
    if not user_id:
        return JSONResponse({"error": "User ID does not exists"}, status_code=400)
    item_id, count = await db.select([Item.id, Item.count]).where(Item.name == data.item_name).gino.first()
    if not item_id:
        return JSONResponse({"error": "Item name does not exist"}, status_code=400)
    if count + data.alteration < 0:
        return JSONResponse({"error": "Count item below 0"}, status_code=400)
    await History.create(user_id=data.user_id, item_id=item_id, alteration=data.alteration)
    await Item.update.values(count=Item.count + data.alteration).where(Item.id == item_id).gino.status()
    return JSONResponse({"message": "History already saved"})


@app.get("/get_history_by_item_name")
async def get_history_by_item_id(item_name: str, page: int = 1):
    response = await db.select([*History, Item.name]).select_from(
        History.join(Item, History.item_id == Item.id)
    ).where(Item.name == item_name).gino.all()
    count_pages = int(len(response) / 10) if len(response) % 10 == 0 else int(len(response) // 10 + 1)
    return JSONResponse({
        "count_pages": count_pages,
        "current_page": page,
        "history": [{
            "user_id": x.user_id,
            "item_name": x.name,
            "alteration": x.alteration,
            "created_at": int(x.created_at.timestamp())
        } for x in response[(page - 1) * 10:page * 10]]
    })


@app.get("/get_all_items")
async def get_all_items(page: int = 1):
    response = await db.select([Item.name, Item.count]).gino.all()
    count_pages = int(len(response) / 10) if len(response) % 10 == 0 else int(len(response) // 10 + 1)
    return JSONResponse({
        "count_pages": count_pages,
        "current_page": page,
        "items": [{
            "item_name": x.name,
            "count": x.count
        } for x in response[(page - 1) * 10:page * 10]]
    })
