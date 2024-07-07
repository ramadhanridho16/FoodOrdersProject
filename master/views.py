import asyncio
import logging
import time

from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from FoodOrdersProject import utils, static_message
from FoodOrdersProject.exception import ResponseStatusError
from FoodOrdersProject.utils import generic_response
from authentication import jwt_utils
from master import service
from master.models import Categories
from .serializer import Test

# Create your views here.

logger = logging.getLogger(__name__)
uuid = utils.uuidv4


@api_view(["GET"])
def categories(req, *args, **kwargs):
    jwt_utils.check_jwt_token(req.headers)

    response = service.get_all_category()
    return generic_response(response, static_message.SUCCESS_GET_LIST.format("category", response["total_data"]),
                            status.HTTP_200_OK)


@api_view(["POST"])
def image_test(request, *args, **kwargs):
    if request.method == "POST":
        file = request.FILES["image"]
        utils.move_file(file, request.POST["destination"])
        return utils.generic_response(
            message=f"Oke, file : {file.content_type} {file.name} {type(file.size)}",
            status_code=status.HTTP_200_OK,
        )


@api_view(["GET"])
def index(request, *args, **kwargs):
    if request.method == "GET":
        print(kwargs)
        logger.info("Tetsing")
        data = {"name": ""}
        test = Test(data=data)
        logger.info(test.is_valid(raise_exception=True))
        return utils.generic_response(message="Oke", status_code=200, data=test.data)


@api_view(["GET"])
def test_exception(request):
    raise ResponseStatusError("test", 400)
    return generic_response(message="Test", status_code=200)


async def test_async(request, name):
    if request.method == "GET":
        category = Categories()
        category.id = uuid()
        category.name = "Drinks"
        await category.asave()
        logger.info(settings.JWT_SECRET_KEY)
        asyncio.create_task(testing_sleep(name))
        return JsonResponse(status=201, data={"Message": name})


@sync_to_async(thread_sensitive=False)
def testing_sleep(name):
    logger.info(name)
    time.sleep(10)
    logger.info(name)
