from django.conf import settings
from django.shortcuts import redirect, render
from django.utils import translation


def index(request):
    if request.user.is_authenticated:
        return redirect('subjects:subject-list')
    else:
        return render(request, 'homepage.html')


def setlang(request, langcode):
    next = request.GET.get('next', '/')
    translation.activate(langcode)
    response = redirect(next)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, langcode)
    return response
