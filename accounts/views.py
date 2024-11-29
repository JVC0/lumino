from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from users.models import Profile

from .forms import LoginForm, SignupForm


def user_login(request):
    FALLBACK_REDIRECT = reverse('shared:homepage')

    if request.user.is_authenticated:
        return redirect(FALLBACK_REDIRECT)
    login_error = False
    if request.method == 'POST':
        next = request.POST.get('next')
        form = LoginForm(request.POST)
        username = form.data['username']
        password = form.data['password']
        if user := authenticate(request, username=username, password=password):
            login(request, user)
            return redirect(next)
        else:
            form = LoginForm()
            login_error = True
    else:
        next = request.GET.get('next', FALLBACK_REDIRECT)
        form = LoginForm()
    return render(
        request,
        'accounts/login.html',
        dict(
            form=form,
            next=next,
            login_error=login_error,
        ),
    )


def user_logout(request):
    logout(request)
    return redirect('shared:homepage')


def user_signup(request):
    if request.method == 'POST':
        if (form := SignupForm(request.POST)).is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('shared:homepage')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', dict(form=form))
