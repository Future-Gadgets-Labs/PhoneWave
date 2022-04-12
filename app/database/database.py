import mongoengine

from app.exceptions import BadConfig
from app.utilities import logger
from app.config import config
from app.database.models import Member


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


def get_member(gid, uid):
    logger.warning("get_member is deprecated. Use Member.get_member instead.")

    member = Member.objects(uid=uid, gid=gid).first()
    if not member:
        member = Member(uid=uid, gid=gid, xp=0, level=0)
        member.save()

    return member
