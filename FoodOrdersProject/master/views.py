from rest_framework.decorators import api_view
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from FoodOrdersProject import utils
from .serializer import Test
import logging
import asyncio
import time
from subprocess import call

# Create your views here.

logger = logging.getLogger(__name__)

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
        return utils.generic_response(message="Oke", status_code=200, data=test.data)
    

async def test_async(request, *args, **kwargs):
    if request.method == "GET":
        name = kwargs['name']
        asyncio.create_task(testing_sleep(name))
        return JsonResponse(status=201, data={"Message":name})
    

@sync_to_async(thread_sensitive=False)
def testing_sleep(name):
    logger.info(name)
    time.sleep(2)
    logger.info(name)