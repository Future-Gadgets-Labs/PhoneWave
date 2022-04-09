from mongoengine import *


class Role(EmbeddedDocument):
    role_id = LongField(required=True)
    channel_id = LongField(required=True)
    message_id = LongField(required=True)
    emoji_id = LongField(required=True)
