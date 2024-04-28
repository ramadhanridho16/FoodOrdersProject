from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from . import models
from FoodOrdersProject import utils
import logging

# Create your views here.

logger = logging.getLogger(__name__)

@api_view(["GET"])
def index(request, *args, **kwargs):
    if request.method == "GET":
        queryset = models.Categories.objects.all()
        logger.info("Test")
        logger.info(queryset)
        return utils.generic_response(message="Oke", status_code=200)
