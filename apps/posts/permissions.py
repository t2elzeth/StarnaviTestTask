from rest_framework.permissions import BasePermission

from .exceptions import QueryParamsNotProvided


class QueryParamsProvided(BasePermission):
    def has_permission(self, request, view):
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if date_from is None or date_to is None:
            raise QueryParamsNotProvided()

        return True
