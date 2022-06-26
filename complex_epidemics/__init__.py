# -*- coding: utf-8 -*-

# TODO: Escrever descrição do pacote
"""_summary_
"""

import datetime
import errno
import logging
import logging.config
import os


LOG_DIR = f"{os.getcwd()}/log"
LOG_FILENAME_PREFIX = __name__
LOG_FILENAME_SUFFIX = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILENAME = f"{LOG_FILENAME_PREFIX}_{LOG_FILENAME_SUFFIX}"
LOG_FULL_PATH = f"{LOG_DIR}/{LOG_FILENAME}.log"


def mkdir_p(path: str) -> None:
    """Directory generator.

    Parameters
    ----------
    path : str
        Directory path to be created.
    """

    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


mkdir_p(LOG_DIR)

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "file_fmt": {
                "format": "%(asctime)s %(name)s — %(levelname)s : %(message)s"
            },
            "console_fmt": {"format": "%(name)s — %(levelname)s : %(message)s"},
        },
        "handlers": {
            "console_handler": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "console_fmt",
            },
            "file_handler": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": LOG_FULL_PATH,
                "formatter": "file_fmt",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console_handler", "file_handler"],
                "level": "DEBUG",
                "propagate": True,
            }
        },
    }
)

LOG = logging.getLogger(__name__)

LOG.info("Initializing.")
LOG.info(f"Execution logs are being created and saved at: {LOG_FULL_PATH} .")
