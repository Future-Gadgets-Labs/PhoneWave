import mongoengine

from app.exceptions import BadConfig
from app.utilities import logger
from app.config import config
from app.database.models import Guild, Member


def init():
    if not config.MONGO_DB:
        raise BadConfig("MONGO_DB is not set.")

    if not config.MONGO_URI:
        raise BadConfig("MONGO_URI is not set.")

    try:
        mongoengine.connect(db=config.MONGO_DB, host=config.MONGO_URI)
        logger.info("MongoDB connected successfully.")
    except Exception as e:
        logger.critical(e)
        exit(1)


def get_guild(gid):
    guild = Guild.objects(gid=gid).first()
    if not guild:
        guild = Guild(gid=gid)
        guild.save()

    return guild


def get_member(gid, uid, create_if_doesnt_exists=True):
    logger.warning("get_member is deprecated. Use Member.get_member instead.")

    member = Member.objects(uid=uid, gid=gid).first()
    if not member and create_if_doesnt_exists:
        member = Member(uid=uid, gid=gid)
        member.save()

    return member


def get_member_by_labmem_number(gid, lab_member_number):
    return Member.objects(gid=gid, lab_member_number=lab_member_number).first()


def get_next_lab_member_number():
    return -1  # TODO
