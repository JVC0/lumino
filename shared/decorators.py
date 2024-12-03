from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from echos.models import Echo
from users.models import Profile
from waves.models import Wave


def echo_validation(func):
    @login_required
    def wrapper(*args, **kwargs):
        user = args[0].user
        echo = Echo.objects.get(pk=kwargs['echo_id'])
        if user != echo.user:
            return HttpResponseForbidden('No puedes modificar el echo de otro usuario.')
        return func(*args, **kwargs)

    return wrapper


def wave_validation(func):
    @login_required
    def wrapper(*args, **kwargs):
        user = args[0].user
        wave = Wave.objects.get(pk=kwargs['wave_id'])
        if user != wave.user:
            return HttpResponseForbidden('No puedes modificar el wave de otro usuario.')
        return func(*args, **kwargs)

    return wrapper


def profile_validation(func):
    @login_required
    def wrapper(*args, **kwargs):
        user = args[0].user
        username = kwargs.get('username')
        profile_user = User.objects.get(username=username)
        profile = Profile.objects.get(user=profile_user)
        if user != profile.user:
            return HttpResponseForbidden('No puedes modificar el perfil de otro usuario.')
        return func(*args, **kwargs)

    return wrapper
