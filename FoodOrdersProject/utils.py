from rest_framework.response import Response
import uuid


def generic_response(data=None, message=None, status_code=200):
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
