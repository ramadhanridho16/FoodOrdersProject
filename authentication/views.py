import logging

from rest_framework.decorators import api_view

from FoodOrdersProject.utils import generic_response
from .jwt_utils import generate_jwt_token, check_jwt_token

# Create your views here.

logger = logging.getLogger(__name__)


@api_view(["POST"])
def login(request, *args, **kwargs):
    if request.method == "POST":
        data = {
            "token": generate_jwt_token(email="asgr397")
        }
        return generic_response(message="Success login", status_code=200, data=data)


@api_view(["GET"])
def check(request, *args, **kwargs):
    if request.method == "GET":
        payload = check_jwt_token(request.headers)
        logger.info(f'Username: {payload["username"]} is access')
        return generic_response(message="Success get data", status_code=200, data=payload)
