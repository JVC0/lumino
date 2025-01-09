from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from subjects.models import Subject 
from users.models import Profile



def teacher_validation(func):
    @login_required
    def wrapper(*args, **kwargs):
        user = args[0].user
        Subject_teacher = Subject.objects.get(code=kwargs['code']).teacher
        if user == Subject_teacher:
            return HttpResponseForbidden('No eres el profesor de esta asignatura')
        return func(*args, **kwargs)

    return wrapper


def wave_validation(func):
    @login_required
    def wrapper(*args, **kwargs):
        user = args[0].user
        wave =objects.get(pk=kwargs['wave_id'])
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
