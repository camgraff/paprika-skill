import aiohttp
import gzip
import json
from mycroft.util.log import LOG

logger = LOG.create_logger(__name__)

class PaprikaClient():
    def __init__(self, username: str, pwd: str) -> None:
        self.username = username
        self.pwd = pwd
        self.auth = aiohttp.BasicAuth(username, pwd)

    async def add_item_to_list(self, item: str):
        grocery_items = [{
          "uid": "randomnumber",
          "order_flag": 428,
          "ingredient": item,
          "separate": False,
          "recipe": None,
          "recipe_uid": None,
          "purchased": False,
          "list_uid": "9E12FCF54A89FC52EA8E1C5DA1BDA62A6617ED8BDC2AEB6F291B93C7A399F6F6",
          "quantity": "",
          "name": item
        }]
        logger.info(json.dumps(grocery_items).encode('utf_8'))
        data = gzip.compress(json.dumps(grocery_items).encode('utf_8'))
        formdata = aiohttp.FormData()
        formdata.add_field("data", data)

        async with aiohttp.ClientSession() as session:
            async with session.post("https://www.paprikaapp.com/api/v1/sync/groceries/", data=formdata, auth=self.auth) as resp:
                resp_text = await resp.text()
                logger.info(f"Paprika response: {resp.status} {resp_text}") 




