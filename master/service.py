# This section contains business logics for master module
import logging

from rest_framework import status

from FoodOrdersProject import utils, static_message
from FoodOrdersProject.exception import ResponseStatusError
from master.models import Categories

uuid = utils.uuidv4
logger = logging.getLogger(__name__)


def get_all_category():
    categories = Categories.objects.all().order_by("id").values()
    logger.info(categories)
    return {
        "categories": categories,
        "total_data": len(categories)
    }


def get_category_by_id(id):
    category = Categories.objects.filter(id=id).first()
    if not category:
        raise ResponseStatusError(static_message.NOT_FOUND_GET_DETAIL.format("Category"),
                                  status=status.HTTP_404_NOT_FOUND)

    return category.to_dict()


def add_category(name):
    category = Categories()
    category.id = uuid()
    category.name = name
    category.save()
    return {
        "id": category.id,
        "name": category.name
    }
