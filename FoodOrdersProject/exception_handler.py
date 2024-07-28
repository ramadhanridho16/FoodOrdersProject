import logging
import traceback

from django.http import JsonResponse
from rest_framework import status

from . import static_message
from .utils import generic_response

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
    logger.warning(f'Handling ResponseStatusError with message : {exc.message} and status : {exc.status}')
    return generic_response(message=exc.message, status_code=exc.status)


def validation_error(exc):
    response_data = {}

    error_dict = list(list(exc.__dict__.values()))[0]
    for i in error_dict:
        response_data[i] = error_dict[i][0].title()

    return generic_response(message="Bad Request", data=response_data, status_code=status.HTTP_400_BAD_REQUEST)


async def async_custom_exception_handler(exc):
    handlers = {
        'ResponseStatusError': async_response_status_error,
        'ValidationError': async_validation_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return await handlers[exception_class](exc)


async def async_response_status_error(exc):
    logger.warning(f'Handling ResponseStatusError with message : {exc.message} and status : {exc.status}')
    response = {"message": exc.message}
    return JsonResponse(data=response, status=exc.status)


async def async_validation_error(exc):
    response_data = {}

    error_dict = list(list(exc.__dict__.values()))[0]
    for i in error_dict:
        response_data[i] = error_dict[i][0].title()

    response = {"message": static_message.BAD_REQUEST, "data": response_data}
    return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST)


async def async_server_error_handler():
    response = {"message": static_message.SERVER_ERROR}
    traceback.print_exc()
    return JsonResponse(
        data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
