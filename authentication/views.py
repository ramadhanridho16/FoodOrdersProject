import asyncio
import json
import logging
import traceback

from asgiref.sync import sync_to_async
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from FoodOrdersProject import static_message
from FoodOrdersProject.utils import generic_response
from . import service
from .jwt_utils import check_jwt_token
from .models import Users, UserVerifies
from .serializer import RegisterRequest, LoginRequest

# Create your views here.

logger = logging.getLogger(__name__)


# Registration method
async def registration(req, *args, **kwargs):
    if req.method == "POST":

        request = RegisterRequest(data=json.loads(req.body))

        try:
            request.is_valid(raise_exception=True)
            request = request.data
        except Exception as exc:
            if exc.__class__.__name__ == "ValidationError":
                data = {}

                error_dict = list(list(exc.__dict__.values()))[0]
                for i in error_dict:
                    data[i] = error_dict[i][0].title()

                response = {"message": static_message.BAD_REQUEST, "data": data}

                return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST)

            response = {"message": static_message.SERVER_ERROR}
            traceback.print_exc()
            return JsonResponse(
                data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            data = await service.register(request)
        except Exception as exc:
            if exc.__class__.__name__ == "ResponseStatusError":
                logger.warn(
                    f"Handling ResponseStatusError with message : {exc.message} and status : {exc.status}"
                )
                response = {"message": exc.message}
                return JsonResponse(data=response, status=exc.status)

            await asyncio.create_task(delete_user_and_user_verify(request))
            response = {"message": static_message.SERVER_ERROR}
            traceback.print_exc()
            return JsonResponse(
                data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return JsonResponse(
            status=201,
            data={"data": data, "message": static_message.SUCCESS_REGISTER},
        )


@api_view(["POST"])
def login(req, *args, **kwargs):
    if req.method == "POST":
        request = LoginRequest(data=json.loads(req.body))
        request.is_valid(raise_exception=True)
        request = request.data

        token = service.login(request)
        response = {
            "token": token
        }
        return generic_response(message=static_message.LOGIN_SUCCESS, status_code=200, data=response)


@api_view(["GET"])
def check(req, *args, **kwargs):
    if req.method == "GET":
        payload = check_jwt_token(req.headers)
        logger.info(f'Username: {payload["username_email"]} is access')
        return generic_response(
            message="Success get data", status_code=200, data=payload
        )


@sync_to_async(thread_sensitive=False)
def delete_user_and_user_verify(request):
    user_verify = UserVerifies.objects.select_related("user").filter(user__username=request["username"])
    user_verify.delete()

    user = Users.objects.filter(username=request["username"])
    user.delete()
