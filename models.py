from typing import List
from pydantic import BaseModel

class Endpoints:
    BASE = "https://www.paprikaapp.com"
    _BASE_API = BASE + "/api/v1/sync"
    # NOTE: the trailing slash is required otherwise the request is routed incorrectly :)
    GROCERIES = _BASE_API + "/groceries/"
    GROCERY_LISTS = _BASE_API + "/grocerylists/"

class GroceryList(BaseModel):
    is_default: bool
    order_flag: int
    uid: str
    reminders_list: str
    name: str

class GroceryListResp(BaseModel):
    result: List[GroceryList]
