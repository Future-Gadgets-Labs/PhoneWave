from mongoengine import *


class Member(Document):
    gid           = LongField(null=False, required=True)
    uid           = LongField(null=False, required=True, primary_key=True, unique_with=["gid"])
    xp            = LongField(default=0)
    level         = LongField(default=0)
    display_name  = StringField()
    name          = StringField()
    discriminator = LongField()
    joined_at     = DateTimeField()
    lab_member_number = LongField()
    is_active     = BooleanField(null=True, default=True)
    is_veteran    = BooleanField(null=True)
