import logging

from .utils import generic_response
from rest_framework import status

# Handling exception

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    handlers = {
        'ResponseStatusError': response_status_error,
        'ValidationError': validation_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc)


def response_status_error(exc):
    logger.warn(f'Handling ResponseStatusError with message : {exc.message} and status : {exc.status}')
    return generic_response(message=exc.message, status_code=exc.status)


def validation_error(exc):
    response_data = {}

    error_dict = list(list(exc.__dict__.values()))[0]
    for i in error_dict:
        response_data[i] = error_dict[i][0].title()

    return generic_response(message="Bad Request", data=response_data, status_code=status.HTTP_400_BAD_REQUEST)
