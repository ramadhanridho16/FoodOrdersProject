import logging

from .utils import generic_response

# Handling exception

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    handlers = {
        'ResponseStatusError': response_status_error,
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc)


def response_status_error(exc):
    logger.warn(f'Handling ResponseStatusError with message : {exc.message} and status : {exc.status}')
    return generic_response(message=exc.message, status_code=exc.status)
