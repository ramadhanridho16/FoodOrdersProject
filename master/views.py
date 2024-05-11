import asyncio
import logging
import time

from asgiref.sync import sync_to_async
from django.http import JsonResponse
from rest_framework.decorators import api_view

from FoodOrdersProject.utils import generic_response, uuidv4
from .models import Categories
from .serializer import Test

# Create your views here.

logger = logging.getLogger(__name__)
uuid = uuidv4


@api_view(["GET"])
def index(request, *args, **kwargs):
    if request.method == "GET":
        print(kwargs)
        logger.info("Tetsing")
        data = {
            "name": ""
        }
        test = Test(data=data)
        logger.info(test.is_valid(raise_exception=True))
        return generic_response(message="Oke", status_code=200, data=test.data)


async def test_async(request, name):
    if request.method == "GET":
        category = Categories()
        category.id = uuid()
        category.name = "Drinks"
        await category.asave()
        asyncio.create_task(testing_sleep(name))
        return JsonResponse(status=201, data={"Message": name})


@sync_to_async(thread_sensitive=False)
def testing_sleep(name):
    logger.info(name)
    time.sleep(10)
    logger.info(name)
