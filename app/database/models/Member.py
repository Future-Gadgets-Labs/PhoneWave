from mongoengine import *


class Member(Document):
    gid = LongField(required=True)
    uid = LongField(required=True, primary_key=True, unique_with=["gid"])
