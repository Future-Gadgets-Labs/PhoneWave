from mongoengine import *


class Announcements(EmbeddedDocument):
    channel_id = LongField()
    welcome = StringField()
    farewell = StringField()
