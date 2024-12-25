from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import EditProfileForm


@login_required
def user_detail(request, username):
    target_user = User.objects.get(username=username)
    return render(
        request,
        'users/user-detail.html',
        {'target_user': target_user},
    )


@login_required
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


@login_required
def leave(request):
    user = request.user
    user.delete()
    return redirect('shared:homepage')
