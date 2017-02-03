from pywps import configuration

import logging
LOGGER = logging.getLogger("PYWPS")


def archive_root():
    return configuration.get_config_value("cache", "archive_root")
