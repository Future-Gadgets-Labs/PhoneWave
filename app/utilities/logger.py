from io import StringIO
from logging.config import dictConfig
import logging
import sys
import warnings

from structlog.dev import CYAN, MAGENTA, plain_traceback, _pad
from structlog.types import EventDict, WrappedLogger
import structlog

LEVEL_TRACE = 5


class PhoneWaveRenderer(structlog.dev.ConsoleRenderer):
    def __call__(self, logger: WrappedLogger, name: str, event_dict: EventDict) -> str:
        sio = StringIO()

        ts = event_dict.pop("timestamp", None)
        if ts is not None:
            sio.write(self._styles.timestamp + str(ts) + self._styles.reset + " ")

        level = event_dict.pop("level", None)
        if level is not None:
            sio.write("| " + self._level_to_color.get(level, "") + _pad(level, self._longest_level) + self._styles.reset + "| ")

        # force event to str for compatibility with standard library
        event = event_dict.pop("event", None)
        if not isinstance(event, str):
            event = str(event)

        if event_dict:
            event = _pad(event, self._pad_event) + self._styles.reset + " "
        else:
            event += self._styles.reset

        sio.write(self._styles.bright + event)

        logger_name = event_dict.pop("logger", None)
        if logger_name is None:
            logger_name = event_dict.pop("logger_name", None)

        if logger_name is not None:
            sio.write("[" + self._styles.logger_name + self._styles.bright + logger_name + self._styles.reset + "] ")

        stack = event_dict.pop("stack", None)
        exc = event_dict.pop("exception", None)
        exc_info = event_dict.pop("exc_info", None)
        sio.write(
            " ".join(
                self._styles.kv_key
                + key
                + self._styles.reset
                + "="
                + self._styles.kv_value
                + self._repr(event_dict[key])
                + self._styles.reset
                for key in sorted(event_dict.keys())
            )
        )

        if stack is not None:
            sio.write("\n" + stack)
            if exc_info or exc is not None:
                sio.write("\n\n" + "=" * 79 + "\n")

        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

            self._exception_formatter(sio, exc_info)

        elif exc is not None:
            if self._exception_formatter is not plain_traceback:
                warnings.warn("Remove `format_exc_info` from your processor chain " "if you want pretty exceptions.")
            sio.write("\n" + exc)

        return sio.getvalue()


logger_styles = PhoneWaveRenderer.get_default_level_styles()
logger_styles["debug"] = MAGENTA
logger_styles["info"] = CYAN

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    PhoneWaveRenderer(pad_event=50, level_styles=logger_styles),
                ],
                "foreign_pre_chain": [
                    structlog.stdlib.add_log_level,
                    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.UnicodeDecoder(),
                ],
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": """
                    asctime: %(asctime)s
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    message: %(message)s
                    module: %(module)s
                    msec: %(msecs)d
                    name: %(name)s
                    pathname: %(pathname)s
                    process: %(process)d
                    processName: %(processName)s
                    relativeCreated: %(relativeCreated)d
                    thread: %(thread)d
                    threadName: %(threadName)s
                    exc_info: %(exc_info)s
                """,
            },
        },
        "handlers": {
            "console_output": {
                "class": "logging.StreamHandler",
                "formatter": "colored",
            },
            "file_output": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": "./app/logs/debug.log",
                "backupCount": 2,
            },
        },
        "loggers": {
            "phonewave": {
                "level": "DEBUG",
                "handlers": ["file_output", "console_output"],
                "propagate": False,
            },
        },
    }
)

logger = logging.getLogger("phonewave")
