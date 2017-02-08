import os

from pywps import configuration

import logging
LOGGER = logging.getLogger("PYWPS")


def archive_root():
    return configuration.get_config_value("cache", "archive_root")


def esmval_root():
    return os.path.join(os.path.dirname(__file__), '..', '..')
