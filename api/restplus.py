from system import config
from system import variables
from system.logger import Logger

from flask_restplus import Api

from api.response import Response

api = Api(version="1.0", title=f"{variables.SERVICE_LABEL} API",
          description="detector_restful_api.")


@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    Logger.exception(f"{message} {e}")

    if not config.FLASK_DEBUG:
        return Response.error(message)
