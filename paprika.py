import gzip
import json
from typing import Dict, List, Optional
from uuid import uuid4

import aiohttp
from mycroft.util.log import LOG
from pydantic import parse, parse_obj_as

from .models import (
    Endpoints,
    GroceryAisle,
    GroceryAislesResp,
    GroceryList,
    GroceryListResp,
)


class PaprikaClient:
    def __init__(self, username: str, pwd: str) -> None:
        self.username = username
        self.pwd = pwd
        self.auth = aiohttp.BasicAuth(username, pwd)
        self.session = aiohttp.ClientSession(auth=self.auth)
        self.grocery_lists: List[GroceryList] = []
        self.default_grocery_list: Optional[GroceryList] = None
        self.grocery_aisle_names: Dict[str, GroceryAisle] = {}

    async def initialize(self) -> None:
        await self.load_grocery_lists()
        await self.load_grocery_aisles()

    async def load_grocery_lists(self) -> None:
        async with self.session.get(Endpoints.GROCERY_LISTS) as resp:
            LOG.info(f"Got grocery_list response: {resp}")
            self.grocery_lists = GroceryListResp.parse_raw(await resp.text()).result
        self.default_grocery_list = next(
            (x for x in self.grocery_lists if x.is_default), None
        )
        LOG.info(f"Setting default grocery list: {self.default_grocery_list}")

    async def load_grocery_aisles(self) -> None:
        async with self.session.get(Endpoints.GROCERY_AISLES) as resp:
            LOG.info(f"Got grocery_aisles response: {resp}")
            aisles = GroceryAislesResp.parse_raw(await resp.text()).result
            self.grocery_aisle_names = {x.name: x for x in aisles}

    def get_aisle_id(self, item: str) -> Optional[str]:
        itm = item.lower()

        def aisle(name: str):
            return self.grocery_aisle_names[name].uid

        if "sauce" in itm or "ketchup" in itm or "mustard" in itm:
            return aisle("Sauces and Condiments")

        if itm.endswith("bread") or itm.endswith("cereal"):
            return aisle("Breads and Cereals")

        if itm.endswith("stock") or itm.endswith("broth"):
            return aisle("Canned and Jar Goods")

        if "chicken" in itm or "beef" in itm or "pork" in itm or "lamb" in itm:
            return aisle("Meat")

        if "fish" in itm:
            return aisle("Seafood")

    async def add_item_to_list(self, item: str, list_id: Optional[str] = None) -> bool:
        """
        Returns true if the item is successfully added, false otherwise
        """

        if list_id is None:
            if self.default_grocery_list is None:
                LOG.error("No default grocery list. Unable to add item.")
                return False
            list_id = self.default_grocery_list.uid

        grocery_items = [
            {
                "uid": str(uuid4()),
                "order_flag": 428,
                "ingredient": item,
                "separate": False,
                "recipe": None,
                "recipe_uid": None,
                "purchased": False,
                # Eventually, it would be cool to enable adding items to different lists
                "list_uid": list_id,
                "quantity": "",
                "name": item,
            }
        ]

        aisle_id = self.get_aisle_id(item)
        if aisle_id is not None:
            grocery_items[0]["aisle_uid"] = aisle_id

        data = gzip.compress(json.dumps(grocery_items).encode("utf_8"))
        formdata = aiohttp.FormData()
        formdata.add_field("data", data)

        async with self.session.post(Endpoints.GROCERIES, data=formdata) as resp:
            resp_text = await resp.text()
            LOG.info(f"Paprika response: {resp.status} {resp_text}")

        return True

    async def close(self) -> None:
        await self.session.close()
