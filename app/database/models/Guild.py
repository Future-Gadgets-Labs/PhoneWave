from mongoengine import *


class Guild(Document):
    gid = LongField(required=True, primary_key=True)
    prefix = StringField()
