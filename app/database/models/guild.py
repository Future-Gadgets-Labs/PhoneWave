from mongoengine import *

from .announcements import Announcements
from .role import Role


class Guild(Document):
    gid = LongField(required=True, primary_key=True)
    prefix = StringField()
    roles = EmbeddedDocumentListField(Role, default=[])
    announcements = EmbeddedDocumentField(Announcements, default=Announcements())
