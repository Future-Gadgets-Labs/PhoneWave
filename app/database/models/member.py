from mongoengine import *


class Member(Document):
    gid = LongField(required=True)
    uid = LongField(required=True, primary_key=True, unique_with=["gid"])
    xp = LongField(default="0")
    level = LongField(default="0")

    def __str__(self) -> str:
        return f"Member(gid={self.gid}, uid={self.uid}, xp={self.xp}, level={self.level})"

    @classmethod
    def get_member(cls, gid: int, uid: int, create=True) -> "Member":
        """Get a member from the database.

        Args:
            gid (int): The guild ID.
            uid (int): The user ID.
            create (bool, optional): Whether to create the member if it doesn't exist. Defaults to True.

        Returns:
            Member: The member.
            None: If the member doesn't exist, and create is False.
        """

        if not gid or not uid:
            raise ValueError("gid or uid must be none-zero.")

        if create:
            return cls.objects.upsert_one(gid=gid, uid=uid)

        object = cls.objects(gid=gid, uid=uid)

        if object.count() == 0:
            return None
        else:
            return object.get.first()
