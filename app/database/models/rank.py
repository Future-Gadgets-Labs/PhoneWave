from mongoengine import Document, IntField, LongField, StringField

from discord.guild import Guild
from discord.utils import get as find

class Rank(Document):
    level = IntField(null=False, required=True, primary_key=True, unique_with=["gid"])
    gid = LongField(null=False, required=True)
    role_id = LongField(null=False, required=True)
    message = StringField()

    def __str__(self):
        return f"Rank(level={self.level}, gid={self.gid}, role_id={self.role_id})"

    @classmethod
    def get_rank(cls, guild: Guild, level:int = None, role_id:int|str = None, create:bool = False) -> "Rank":
        """Get a member from the database.

        Args:
            guild (Guild): The guild.
            level (int): The level for the rank.
            role_id (int|str, optional): The role id or name. Can be used in place of level for getting if it exists.
            create (bool, optional): Whether to create the rank if it doesn't exist. Defaults to False.

        Returns:
            Rank: The rank.
            None: If the rank doesn't exist, and create is False.
        """

        if not guild or not (level or role_id):
            raise ValueError("guild and level or role_id must be filled.")

        if isinstance(role_id, str):
            role_id = find(guild.roles, name=role_id).id

        rank = None

        if level is None:
            rank = cls.objects(gid=guild.id, role_id=role_id).first()
        elif role_id is None:
            rank = cls.objects(gid=guild.id, level=level).first()

        if rank is None and create:
            if role_id is None:
                raise ValueError(f"Trying to create Rank but invalid role id provided: {role_id}")

            rank = Rank(gid=guild.id, level=level, role_id=role_id)
            rank.save()
        
        return rank