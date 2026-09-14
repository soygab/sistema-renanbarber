from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(role):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.user.is_superuser or request.user.role == role:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("Seu perfil não possui acesso a esta área.")

        return wrapped

    return decorator


client_required = role_required("client")
barber_required = role_required("barber")
