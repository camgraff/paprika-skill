from typing import List
from pydantic import BaseModel

class Endpoints:
    BASE = "https://www.paprikaapp.com"
    _BASE_API = BASE + "/api/v1/sync"
    # NOTE: the trailing slash is required otherwise the request is routed incorrectly :)
    GROCERIES = _BASE_API + "/groceries/"
    GROCERY_LISTS = _BASE_API + "/grocerylists/"
    GROCERY_AISLES = _BASE_API + "/groceryaisles/"

class GroceryList(BaseModel):
    is_default: bool
    order_flag: int
    uid: str
    reminders_list: str
    name: str

class GroceryAisle(BaseModel):
    uid: str
    name: str
    order_flag: int

class GroceryListResp(BaseModel):
    result: List[GroceryList]

class GroceryAislesResp(BaseModel):
    result: List[GroceryAisle]
