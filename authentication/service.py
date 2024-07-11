# This section contains business logics for authentication module
import asyncio
import datetime
import logging
from datetime import timedelta, datetime

import bcrypt
from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.models import Q
from rest_framework import status

from FoodOrdersProject import utils, static_message
from FoodOrdersProject.exception import ResponseStatusError
from authentication import jwt_utils
from authentication.models import Users, UserVerifies

logger = logging.getLogger(__name__)

uuid = utils.uuidv4


async def register(req):
    # Get current time and add 2 hours to it as expired date
    expired_date = datetime.now() + timedelta(hours=2)

    req["expired_date"] = utils.convert_datetime_to_epoch(expired_date)

    # Call this function to save users and user_verifications
    token, user = await asyncio.create_task(save_register(req))

    # After save, call this function to run send email asynchronously
    asyncio.create_task(
        utils.sending_email(
            req["email"],
            {
                "name": req["name"],
                "expired_date": expired_date.strftime("jam %H:%M:%S, tanggal %d-%m-%Y"),
            },
            token,
            static_message.REGISTER,
        )
    )

    return {
        "name": user.name,
        "phone": user.phone,
        "username": user.username,
        "gender": user.gender,
        "birth_date": user.birth_date,
    }


def login(req):
    user = Users.objects.filter(Q(email=req["username_email"]) | Q(username=req["username_email"]))
    if not user.exists():
        raise ResponseStatusError(message=static_message.LOGIN_ERROR, status=status.HTTP_401_UNAUTHORIZED)

    user = user.get()

    is_password_valid = bcrypt.checkpw(req["password"].encode("utf-8"), bytes(user.password, "utf-8"))

    if not is_password_valid:
        raise ResponseStatusError(message=static_message.LOGIN_ERROR, status=status.HTTP_401_UNAUTHORIZED)

    if not user.activate:
        raise ResponseStatusError(message=static_message.NOT_VERIFY, status=status.HTTP_401_UNAUTHORIZED)

    return jwt_utils.generate_jwt_token(req["username_email"])


async def resend_verification(req):
    expired_date = datetime.now() + timedelta(hours=2)

    req["expired_date"] = utils.convert_datetime_to_epoch(expired_date)

    [token, user] = await asyncio.create_task(save_resend_verification(req))

    # After save, call this function to run send email asynchronously
    asyncio.create_task(
        utils.sending_email(
            req["email"],
            {
                "name": user.name,
                "expired_date": expired_date.strftime("jam %H:%M:%S, tanggal %d-%m-%Y"),
            },
            token,
            static_message.RESEND_VERIFY,
        )
    )


@sync_to_async(thread_sensitive=False)
def save_register(req):
    # Check the password is same or not
    check_confirmation_password(req["password"], req["confirmation_password"])

    # Check if the gender is correct
    if req["gender"] not in Users.GenderChoices:
        raise ResponseStatusError(static_message.WRONG_GENDER, status=status.HTTP_400_BAD_REQUEST)

    # Check if username or email is already used
    if (
            Users.objects.filter(
                Q(email=req["email"]) | Q(username=req["username"])
            ).count()
            > 0
    ):
        raise ResponseStatusError(
            static_message.USED_USERNAME_EMAIL, status=status.HTTP_400_BAD_REQUEST
        )

    password = bcrypt.hashpw(req["password"].encode("utf-8"), bcrypt.gensalt())

    # Insert thew user
    user = Users()
    user.username = req["username"]
    user.name = req["name"]
    user.password = password.decode()
    user.phone = req["phone"]
    user.gender = req["gender"]
    user.birth_date = req["birth_date"]
    user.email = req["email"]
    user.save()

    # Insert to user_verifies
    user_verify = UserVerifies()
    user_verify.token = uuid()
    user_verify.expired_at = req["expired_date"]
    user_verify.user = user
    user_verify.save()

    # Return the token
    return [user_verify.token, user]


@sync_to_async(thread_sensitive=False)
def save_resend_verification(req):
    user = Users.objects.filter(email=req["email"])

    if not user.exists():
        raise ResponseStatusError(message=static_message.EMAIL_NOT_EXIST, status=status.HTTP_400_BAD_REQUEST)

    user = user.get()

    if user.activate:
        raise ResponseStatusError(message=static_message.ACCOUNT_ALREADY_ACTIVATE, status=status.HTTP_400_BAD_REQUEST)

    user_verify = user.user_verifies
    user_verify.token = uuid()
    user_verify.expired_at = req["expired_date"]
    user_verify.save()

    # Return the token
    return [user_verify.token, user]


def check_confirmation_password(password, confirmation_password):
    if password != confirmation_password:
        raise ResponseStatusError(
            static_message.PASSWORD_NOT_SAME,
            status=status.HTTP_400_BAD_REQUEST,
        )


def verify(token):
    with transaction.atomic():
        user_verify = UserVerifies.objects.filter(token=token)
        if not user_verify.exists():
            raise ResponseStatusError(message=static_message.NOT_VERIFY, status=status.HTTP_400_BAD_REQUEST)
        user_verify = user_verify.get()

        user = user_verify.user

        if user.activate:
            raise ResponseStatusError(message=static_message.ACCOUNT_ALREADY_ACTIVATE,
                                      status=status.HTTP_400_BAD_REQUEST)

        expired_date = datetime.fromtimestamp(user_verify.expired_at / 1000)

        if datetime.now() > expired_date:
            raise ResponseStatusError(message=static_message.EXPIRED_VERIFICATION_TOKEN,
                                      status=status.HTTP_400_BAD_REQUEST)
        user.activate = True
        user.save()
