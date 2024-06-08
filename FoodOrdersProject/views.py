from django.http import JsonResponse
from rest_framework import status

# Create your views here.

def error_404(request, exception):
    print(request.path)
    return JsonResponse(status=status.HTTP_404_NOT_FOUND, data={"message": f"path {request.path} not found"})

def error_500(request):
    return JsonResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"message": "something wrong with the server"})
