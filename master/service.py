# This section contains business logics for master module
import logging

from master.models import Categories

logger = logging.getLogger(__name__)


def get_all_category():
    categories = Categories.objects.all().order_by("id").values()
    logger.info(categories)
    return {
        "categories": categories,
        "total_data": len(categories)
    }
