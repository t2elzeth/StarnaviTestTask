from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class QueryParamsNotProvided(APIException):
    default_detail = _("Query params not provided")
    status_code = status.HTTP_400_BAD_REQUEST
