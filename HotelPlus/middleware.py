from users.models import SecondaryUser

class SecondaryUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and isinstance(request.user, SecondaryUser):
            proprietaire = request.user.proprietaire
            request.user.groups.set(proprietaire.groups.all())
            request.user.user_permissions.set(proprietaire.user_permissions.all())
        response = self.get_response(request)
        return response