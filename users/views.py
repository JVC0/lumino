from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import EditProfileForm


def user_detail(request, username):
    target_user = User.objects.get(username=username)
    return render(
        request,
        'users/user-detail.html',
        {'target_user': target_user},
    )


def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            profile = form.save(commit=False)

            profile.save()
            return redirect('user-detail', request.user)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit-profile.html', dict(profile=profile, form=form))


def request_certificate(request):
    pass




def leave(request):
    user = request.user
    # if request.method in ['POST', 'GET']:
    user.delete()
    return redirect('shared:homepage')
