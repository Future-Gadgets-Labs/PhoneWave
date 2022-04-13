from mongoengine import *


class Announcements(EmbeddedDocument):
    channel_id = LongField()
    welcome = StringField()
    farewell = StringField()

    def __str__(self) -> str:
        return f"Announcements(channel_id={self.channel_id}, welcome={self.welcome}, farewell={self.farewell})"
