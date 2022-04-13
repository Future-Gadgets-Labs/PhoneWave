from mongoengine import *


class Role(EmbeddedDocument):
    role_id = LongField(required=True)
    channel_id = LongField(required=True)
    message_id = LongField(required=True)
    emoji_id = LongField(required=True)

    def __str__(self) -> str:
        return f"Role(role_id={self.role_id}, channel_id={self.channel_id}, message_id={self.message_id}, emoji_id={self.emoji_id})"
