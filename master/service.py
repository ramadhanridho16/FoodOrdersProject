# This section contains business logics for master module
import logging

from FoodOrdersProject import utils
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


def add_category(name):
    category = Categories()
    category.id = uuid()
    category.name = name
    category.save()
    return {
        "id": category.id,
        'name': category.name
    }
