from datetime import datetime

from mongoengine import *

from app import config
from app.database.models.badge import Badge

class Member(Document):
    gid = LongField(null=False, required=True)
    uid = LongField(null=False, required=True, primary_key=True, unique_with=["gid"])
    xp = IntField(default=0)
    level = IntField(default=0)
    joined_at = DateTimeField()
    lab_member_number = IntField()
    is_active = BooleanField(default=True)
    badges = EmbeddedDocumentListField(Badge, default=[])

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
            raise ValueError("gid and uid must be non-zero")

        mem = cls.objects(gid=gid, uid=uid).first()

        if mem is None and create:
            mem = cls(gid=gid, uid=uid)
            mem.save()

        return mem

    @classmethod
    def get_member_by_labmem_number(cls, gid: int, lab_member_number: int) -> "Member":
        """Find the member with the provided Lab Member Number from the database.

        Args:
            gid (int): The guild ID.
            lab_member_number (int): The lab member ID.

        Returns:
            Member: The member.
            None: If the member doesn't exist.
        """

        if not gid or not lab_member_number:
            raise ValueError("gid and lab_member_number must be filled.")

        return cls.objects(gid=gid, lab_member_number=lab_member_number).first()

    @classmethod
    def get_next_available_lab_member_number(cls) -> int:
        return -1  # TODO

    def is_veteran(self) -> bool:
        if not self.joined_at:
            return False

        veteran_cutoff = datetime.strptime(config.BADGE_VETERAN_CUTOFF_DATE, '%Y-%m-%dT%H:%M:%S%z')

        return self.joined_at < veteran_cutoff 
