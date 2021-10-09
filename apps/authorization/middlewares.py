from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TrackUserLastActiveMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            request.user.last_active = timezone.now()
            request.user.save()
        return response
