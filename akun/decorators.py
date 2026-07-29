from django.shortcuts import redirect
from functools import wraps


def role_required(role):
    """Decorator untuk pembatasan akses berdasarkan Profil.role."""

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            profil = getattr(request.user, 'profil', None)
            if profil is not None and profil.role == role:
                return view_func(request, *args, **kwargs)

            return redirect('login')

        return wrapper

    return decorator

