import datetime
import logging
from datetime import datetime, timezone, timedelta

import jwt
from django.conf import settings

from FoodOrdersProject.exception import ResponseStatusError

secret_key = settings.JWT_SECRET_KEY

logger = logging.getLogger(__name__)

""" 
Function to check if the JWT token is provide or valid for the request
If the token is exist and valid, return the dictionary of the payload in the token
If not rise the exception 
"""


def check_jwt_token(headers):
    jwt_token = None
    
    if "Authorization" in headers:
        jwt_token = headers["Authorization"]

    if (jwt_token is None) or (jwt_token.startswith("Bearer ") is False):
        raise ResponseStatusError("Unauthorized", 401)

    jwt_token = jwt_token.split("Bearer ")[1]
    logger.info(f'Jwt Token is : {jwt_token}')

    try:
        payload = jwt.decode(jwt_token, secret_key, algorithms=["HS256"])
    except Exception:
        raise ResponseStatusError("Unauthorized", 401)

    return payload


"""
Function to generate jwt token from payload using secret key that store in the environment
If success return string of token
"""


def generate_jwt_token(email=None, username=None):
    logger.info(datetime.now(timezone.utc))
    payload = {
        "email": email if email is not None else None,
        "username": username if username else None,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2),
        "iat": datetime.now(timezone.utc),
        "issuer_by": "Food orders system",
    }

    jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")

    return jwt_token
