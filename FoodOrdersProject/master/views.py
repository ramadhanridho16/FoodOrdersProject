from rest_framework.decorators import api_view
from FoodOrdersProject import utils
from .serializer import Test
import logging

# Create your views here.

logger = logging.getLogger(__name__)

@api_view(["GET"])
def index(request, *args, **kwargs):
    if request.method == "GET":
        data = {
            "name": ""
        }

        test = Test(data=data)
        logger.info(test.is_valid(raise_exception=True))
        return utils.generic_response(message="Oke", status_code=200, data=test.data)
