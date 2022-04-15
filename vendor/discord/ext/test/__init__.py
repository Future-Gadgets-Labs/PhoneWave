
__title__ = "testcord"
__author__ = "KoalaBotUK"
__license__ = "MIT"
__copyright__ = "Copyright 2018-2019 CraftSpider & Copyright 2022-present KoalaBotUK"
__version__ = "0.0.1"

from . import backend
from .runner import *
from .utils import embed_eq, activity_eq, embed_proxy_eq, PeekableQueue
from .verify import verify, Verify, VerifyMessage, VerifyActivity
