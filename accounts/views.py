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
    next = request.GET.get('next')

    if request.method == 'POST':
        if (form := LoginForm(request.POST)).is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user := authenticate(request, username=username, password=password):
                login(request, user)

                return redirect(next or FALLBACK_REDIRECT)
            else:
                login_error = True

    else:
        form = LoginForm()
    return render(
        request,
        'accounts/login.html',
        dict(form=form, login_error=login_error, next=next),
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
