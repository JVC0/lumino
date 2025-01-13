from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import EditProfileForm


def teacher_cant_leave(func):
    @login_required
    def wrapper(*args, **kwargs):
        user = args[0].user
        if not user.profile.is_student():
            return HttpResponseForbidden('EL profesor no se puede ir')
        return func(*args, **kwargs)
    return wrapper


@login_required
def user_detail(request, username):
    target_user = User.objects.get(username=username)
    for enrollment in request.user.enrolled.all():
        print(enrollment.mark)
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
            profile.save()
            messages.success(request, 'User profile has been successfully saved.')
            return redirect('user-detail', request.user)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit-profile.html', dict(profile=profile, form=form))


@teacher_cant_leave
def leave(request):
    user = request.user
    messages.success(request, 'Good bye! Hope to see you soon.')
    user.delete()
    return redirect('shared:homepage')
