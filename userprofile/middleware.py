from django.core.cache import cache


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cache.set(f'online_user_{request.user.pk}', True, 3600000)
        response = self.get_response(request)
        return response
