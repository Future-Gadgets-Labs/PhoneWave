from datetime import datetime

from mongoengine import *


class Badge(EmbeddedDocument):
    name = StringField(required=True)
    awarded_on = DateTimeField(default=datetime.utcnow)

    def __str__(self) -> str:
        return f"Badge(name={self.name}, awarded_on={self.awarded_on})"
