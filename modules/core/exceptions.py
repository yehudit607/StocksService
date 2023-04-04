import logging
import traceback
from http import HTTPStatus

from rest_framework.response import Response


def get_session_logger():
    return logging.getLogger("stocks")


logger = get_session_logger()


def general_exception():
    logger.error("general Exception, exception is:")
    traceback.print_exc()
    return Response(
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
