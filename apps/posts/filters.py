from rest_framework.filters import BaseFilterBackend


class LikeAnalyticsFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        return queryset.filter(date_created__gte=date_from, date_created__lte=date_to)
