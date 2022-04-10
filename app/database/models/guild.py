from mongoengine import *

from app.database.models.announcements import Announcements
from app.database.models.role import Role


class Guild(Document):
    gid = LongField(required=True, primary_key=True)
    prefix = StringField()
    roles = EmbeddedDocumentListField(Role, default=[])
    announcements = EmbeddedDocumentField(Announcements, default=Announcements())
