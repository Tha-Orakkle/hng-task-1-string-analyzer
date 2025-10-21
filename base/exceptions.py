from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicateEntryException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "String already exists in the system"
    

class UnprocessableEntityException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Invalid data type for 'value' (must be string)"
    

class MissingValueException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = " Invalid request body or missing 'value' field"
