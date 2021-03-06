import os
from pywps.app.Service import Service

from esmvalwps.processes import processes

__version__ = "1.1.0"


def application(environ, start_response):
    app = Service(processes, [os.environ.get('PYWPS_CFG')])
    return app(environ, start_response)

