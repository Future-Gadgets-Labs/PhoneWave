from mongoengine import *

from .announcements import Announcements
from .role import Role


class Guild(Document):
    gid = LongField(required=True, primary_key=True)
    prefix = StringField()
    roles = EmbeddedDocumentListField(Role, default=[])
    announcements = EmbeddedDocumentField(Announcements, default=Announcements())

    def __str__(self) -> str:
        return f"Guild(gid={self.gid})"

    @classmethod
    def get_guild(cls, gid: int, create=True) -> "Guild":
        """Get a guild from the database.

        Args:
            gid (int): The guild ID.
            create (bool, optional): Whether to create the guild if it doesn't exist. Defaults to True.

        Returns:
            Member: The member.
            None: If the member doesn't exist, and create is False.
        """

        if not gid:
            raise ValueError("gid must be non-zero.")

        if create:
            return cls.objects.upsert_one(gid=gid)

        return cls.objects(gid=gid).first()
