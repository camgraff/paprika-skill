from mycroft import MycroftSkill, intent_handler
import asyncio
from .paprika import PaprikaClient

class Paprika(MycroftSkill):
    def __init__(self):
        super().__init__()

    def initialize(self):
        # TODO: Handle settings change to update auth
        username = self.settings['username']
        password = self.settings['password']
        try: 
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        self.paprika = PaprikaClient(username, password)
        self.loop.run_until_complete(self.paprika.initialize())

    @intent_handler('add.item.intent')
    def handle_add_item(self, message):
        item = message.data.get('item')
        self.loop.run_until_complete(self._handle_add_item(item))

    async def _handle_add_item(self, item: str):
        self.log.info(f"Adding item to list: {item}")
        await self.paprika.add_item_to_list(item)
        self.speak_dialog('paprika')

    def shutdown(self):
        self.loop.run_until_complete(self.paprika.close())


def create_skill():
    return Paprika()

