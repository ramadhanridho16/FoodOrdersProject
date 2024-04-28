from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from . import models
import logging

# Create your views here.

logger = logging.getLogger(__name__)

@api_view(["GET"])
def index(request, *args, **kwargs):
    if request.method == "GET":
        queryset = models.Categories.objects.all()
        logger.info("Test")
        print(queryset)
        return Response(data={"data": "Hello World"}, status=200, content_type="application/json")
