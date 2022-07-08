from rest_framework.exceptions import APIException


class UnknownClientColumns(APIException):
    status_code = 400
    default_detail = 'Unknown columns of client names'
    default_code = 'unknown_client_columns'
