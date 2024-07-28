import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from FoodOrdersProject import static_message
from FoodOrdersProject.exception import ResponseStatusError
from FoodOrdersProject.exception_handler import async_custom_exception_handler, async_server_error_handler
from FoodOrdersProject.utils import generic_response
from authentication import service
from authentication.jwt_utils import check_jwt_token
from authentication.models import Users, UserVerifies
from authentication.serializer import RegisterRequest, LoginRequest, ResendEmailRequest, ChangePasswordRequest

# Create your views here.

logger = logging.getLogger(__name__)


# Registration method
async def registration(req, *args, **kwargs):
    if req.method == "POST":
        data = None
        request = RegisterRequest(data=json.loads(req.body))

        try:
            request.is_valid(raise_exception=True)
            request = request.data
        except Exception as exc:
            error_response = await async_custom_exception_handler(exc)

            if error_response:
                return error_response

            error_response = await async_server_error_handler()

            if error_response:
                return error_response

        try:
            data = await service.register(request)
        except Exception as exc:
            error_response = await async_custom_exception_handler(exc)

            if error_response:
                return error_response

            await asyncio.create_task(delete_user_and_user_verify(request))

            error_response = await async_server_error_handler()

            if error_response:
                return error_response

        return JsonResponse(
            status=201,
            data={"data": data, "message": static_message.SUCCESS_REGISTER},
        )


async def resend_verification(req, *args, **kwargs):
    if req.method == "POST":
        request = ResendEmailRequest(data=json.loads(req.body))

        try:
            request.is_valid(raise_exception=True)
            request = request.data
        except Exception as exc:
            error_response = await async_custom_exception_handler(exc)

            if error_response:
                return error_response

            error_response = await async_server_error_handler()

            if error_response:
                return error_response

        try:
            await service.resend_verification(request)
        except Exception as exc:
            error_response = await async_custom_exception_handler(exc)

            if error_response:
                return error_response

            error_response = await async_server_error_handler()

            if error_response:
                return error_response

        return JsonResponse(
            data={
                "messages": static_message.SUCCESS_RESEND_VERIFICATION
            }, status=status.HTTP_200_OK
        )
    else:
        return JsonResponse(
            data={"message": "Method {} not allowed".format(req.method)}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


async def send_forget_password(req, *args, **kwargs):
    if req.method == "POST":
        request = ResendEmailRequest(data=json.loads(req.body))

        try:
            request.is_valid(raise_exception=True)
            request = request.data
        except Exception as exc:
            error_response = await async_custom_exception_handler(exc)

            if error_response:
                return error_response

            error_response = await async_server_error_handler()

            if error_response:
                return error_response

        try:
            await service.send_forget_password(request)
        except Exception as exc:
            error_response = await async_custom_exception_handler(exc)

            if error_response:
                return error_response

            error_response = await async_server_error_handler()

            if error_response:
                return error_response

        return JsonResponse(
            data={
                "messages": static_message.SUCCESS_SEND_FORGET_PASSWORD
            }, status=status.HTTP_200_OK
        )
    else:
        return JsonResponse(
            data={"message": "Method {} not allowed".format(req.method)}, status=status.HTTP_405_METHOD_NOT_ALLOWED
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


@api_view(["PATCH"])
def verify(req, *args, **kwargs):
    if req.method == "PATCH":
        if "token" not in req.query_params.keys():
            raise ResponseStatusError(message=static_message.NOT_VALID_TOKEN,
                                      status=status.HTTP_400_BAD_REQUEST)

        service.verify(req.query_params["token"])

        return generic_response(message=static_message.VERIFY_ACCOUNT_SUCCESS, status_code=status.HTTP_200_OK)


@api_view(["PATCH"])
def change_password(req, *args, **kwargs):
    if req.method == "PATCH":
        if "token" not in req.query_params.keys():
            raise ResponseStatusError(message=static_message.NOT_VALID_TOKEN,
                                      status=status.HTTP_400_BAD_REQUEST)

        request = ChangePasswordRequest(data=json.loads(req.body))
        request.is_valid(raise_exception=True)
        request = request.data

        service.change_password(request, req.query_params["token"])

        return generic_response(message=static_message.CHANGE_PASSWORD_SUCCESS, status_code=status.HTTP_200_OK)


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
