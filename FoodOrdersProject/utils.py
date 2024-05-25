import logging
import os
import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from FoodOrdersProject.exception import ResponseStatusError

logger = logging.getLogger(__name__)


def generic_response(data=None, message=None, status_code=status.HTTP_200_OK):
    response = {}

    if data == None:
        response = {
            "message": message,
            "status": status_code
        }
    else:
        response = {
            "data": data,
            "message": message,
            "status": status_code
        }

    return Response(response, status_code, content_type="application/json")


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
        raise ResponseStatusError("Destination is not valid", status.HTTP_400_BAD_REQUEST)

    return destination_path


def move_file(file, destination):
    # Check if file is an image
    if file.content_type.split("/")[0] != "image":
        raise ResponseStatusError("Wrong format file, make sure it's a image format", status.HTTP_400_BAD_REQUEST)

    # Check if file over the capacity or not
    if file.size > MAX_FILE_SIZE:
        raise ResponseStatusError("File too large, max size is 5,2 Mb", status.HTTP_400_BAD_REQUEST)

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
    except FileNotFoundError:
        logger.error(f"File {full_path} not found")
        raise ResponseStatusError("Server error", status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"Error {e}")
        raise ResponseStatusError("Server error", status.HTTP_500_INTERNAL_SERVER_ERROR)
