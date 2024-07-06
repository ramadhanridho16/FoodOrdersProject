from django.http import JsonResponse
from rest_framework import status

from FoodOrdersProject import static_message


# Create your views here.

def error_404(request, exception):
    print(request.path)
    return JsonResponse(status=status.HTTP_404_NOT_FOUND,
                        data={"message": static_message.PATH_NOT_FOUND.format(request.path)})


def error_500(request):
    return JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={"message": static_message.SERVER_ERROR})
