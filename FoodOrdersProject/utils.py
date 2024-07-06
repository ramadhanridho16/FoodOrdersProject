import datetime
import logging
import os
import traceback
import uuid
from datetime import timezone, datetime

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.response import Response

from FoodOrdersProject.exception import ResponseStatusError
from . import static_message

logger = logging.getLogger(__name__)


def generic_response(data=None, message=None, status_code=status.HTTP_200_OK):
    response = {}

    if data == None:
        response = {"message": message, "status": status_code}
    else:
        response = {"data": data, "message": message, "status": status_code}

    return Response(response, status_code)


def uuidv4():
    return str(uuid.uuid4())


# File manager utils

MENUS_IMAGE_PATH = os.path.join("static", "images", "menus")
BANNERS_IMAGE_PATH = os.path.join("static", "images", "banners")
MAX_FILE_SIZE = int(settings.MAX_FILE_SIZE)


def get_destination_path(destination):
    if destination == "MENUS":
        destination_path = os.path.join(settings.BASE_DIR, MENUS_IMAGE_PATH)
    elif destination == "BANNERS":
        destination_path = os.path.join(settings.BASE_DIR, BANNERS_IMAGE_PATH)
    else:
        raise ResponseStatusError(
            static_message.DESTINATION_NOT_VALID, status.HTTP_400_BAD_REQUEST
        )

    return destination_path


def move_file(file, destination):
    # Check if file is an image
    if file.content_type.split("/")[0] != "image":
        raise ResponseStatusError(
            static_message.WRONG_FORMAT_FILE,
            status.HTTP_400_BAD_REQUEST,
        )

    # Check if file over the capacity or not
    if file.size > MAX_FILE_SIZE:
        raise ResponseStatusError(
            static_message.FILE_TOO_LARGE.format(round(MAX_FILE_SIZE / 1000000, 1)), status.HTTP_400_BAD_REQUEST
        )

    destination_path = os.path.join(get_destination_path(destination), file.name)
    file_exist = os.path.exists(destination_path)

    if file_exist:
        logger.info("File exist")
        # If file exist delete file first and save the file
        delete_file(full_path=destination_path)

    save_file(file, destination_path)


def save_file(file, full_path):
    destination = open(full_path, "wb+")
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()


def delete_file(full_path=None, file=None, destination=None):
    if file is not None:
        full_path = os.path.join(get_destination_path(destination), file.name)

    logger.info(f"Deleting {full_path}")
    try:
        os.remove(full_path)
    except FileNotFoundError as exc:
        traceback.print_exc()
        logger.error(f"File {full_path} not found")
        raise ResponseStatusError(
            static_message.SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as exc:
        traceback.print_exc()
        logger.error(f"Error {exc}")
        raise ResponseStatusError(
            static_message.SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@sync_to_async(thread_sensitive=False)
def sending_email(to, data, token, event):
    if event == static_message.REGISTER:
        logger.info(f"Start sending email to {to}")
        context = {
            "subjectMessage": "Register",
            "link_destination": f"http://www.{token}.com",
            "message": static_message.BODY.format(data["name"], data["expired_date"]),
            "button": "Verify",
            "year": datetime.now().strftime("%Y"),
        }
        subject = static_message.SUBJECT
        html_message = render_to_string("email_example.html", context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [to],
            html_message=html_message,
        )
        logger.info(f"Done sending email to {to}")
    elif event == static_message.FORGET_PASSWORD:
        pass
    elif event == static_message.RESEND_VERIFY:
        pass


# Convert the expired date to epoch milis and convert it to UTC timezone
def convert_datetime_to_epoch(date):
    expire_milis = date.astimezone(timezone.utc)
    # Get epoch milis by substract with the start of epoch milis date
    expire_milis = expire_milis - datetime(1970, 1, 1, tzinfo=timezone.utc)
    # Multiply the total second with a thousand
    return round(expire_milis.total_seconds() * 1000)
