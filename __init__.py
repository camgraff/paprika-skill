from mycroft import MycroftSkill, intent_handler
import asyncio
from .paprika import PaprikaClient

class Paprika(MycroftSkill):
    def __init__(self):
        super().__init__()

    def initialize(self):
        username = self.settings['username']
        password = self.settings['password']
        self.paprika = PaprikaClient(username, password)

    @intent_handler('add.item.intent')
    def handle_add_item(self, message):
        item = message.data.get('item')
        asyncio.run(self._handle_add_item(item))

    async def _handle_add_item(self, item: str):
        self.log.info(f"Adding item to list: {item}")
        await self.paprika.add_item_to_list(item)
        self.speak_dialog('paprika')



def create_skill():
    return Paprika()

