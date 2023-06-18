import json

from aiohttp import ClientSession

from api_wrapper.serializers import HistoryByItem, AllItems, ExistItem
import msgspec


class APIError(Exception):
    pass


class APIWrapper:

    BASE_URL = "http://127.0.0.1:8001"

    async def _post_request(self, url: str, data: dict, model=None):
        async with ClientSession() as session:
            response = await session.post(f"{self.BASE_URL}/{url}", data=json.dumps(data),
                                          headers={"Content-Type": "application/json"})
            raw_data = await response.read()
        data = self._validate_response(raw_data, model)
        return data

    async def _delete_request(self, url: str, data: dict, model=None):
        async with ClientSession() as session:
            response = await session.delete(f"{self.BASE_URL}/{url}", data=json.dumps(data),
                                            headers={"Content-Type": "application/json"})
            raw_data = await response.read()
        data = self._validate_response(raw_data, model)
        return data

    async def _get_request(self, url: str, data: dict, model=None):
        async with ClientSession() as session:
            response = await session.get(f"{self.BASE_URL}/{url}", params=data)
            raw_data = await response.read()
        data = self._validate_response(raw_data, model)
        return data

    @staticmethod
    def _validate_response(data, model):
        if model:
            return msgspec.json.decode(data, type=model)
        data = json.loads(data)
        if "error" in data:
            raise APIError(data['error'])
        return data

    async def add_item(self, name: str):
        return await self._post_request("add_item", {"name": name})

    async def create_user(self, user_id: int, screen_name: str, full_name: str):
        return await self._post_request("create_user",
                                        {"user_id": user_id, "screen_name": screen_name, "full_name": full_name})

    async def delete_item(self, item_name: str):
        return await self._delete_request("delete_item", {"item_name": item_name})

    async def save_history(self, user_id: int, item_name: str, alteration: int):
        return await self._post_request("save_history", {"user_id": user_id, "item_name": item_name,
                                                         "alteration": alteration})

    async def get_all_items(self, page: int = 1) -> AllItems:
        return await self._get_request("get_all_items", {"page": page}, AllItems)

    async def get_history_by_item_name(self, item_name: str, page: int = 1) -> HistoryByItem:
        return await self._get_request("get_history_by_item_name", {"item_name": item_name, "page": page}, HistoryByItem)

    async def check_item_name(self, item_name: str) -> ExistItem:
        return await self._get_request("check_item_name", {"item_name": item_name}, ExistItem)
