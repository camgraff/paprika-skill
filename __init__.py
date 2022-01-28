from mycroft import MycroftSkill, intent_file_handler


class Paprika(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('paprika.intent')
    def handle_paprika(self, message):
        self.speak_dialog('paprika')


def create_skill():
    return Paprika()

