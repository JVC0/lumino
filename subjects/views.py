from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Lesson, Subject


# Create your views here.
@login_required
def subject_list(request):
    user_profile = request.user.profile
    if user_profile.is_student():
        subjects = Subject.objects.filter(students=request.user)
    else:
        subjects = Subject.objects.filter(teacher=request.user)
    return render(
        request,
        'subjects/subject-list.html',
        dict(user_profile=user_profile, subjects=subjects),
    )


@login_required
def subject_detail(request, code):
    subject_code = Lesson.subject
    lesson = Lesson.objects.get(subject=subject_code)
    return render(request, 'subjects/subject-detail.html', dict(lesson=lesson))


@login_required
def subject_lessons(request):
    pass


@login_required
def lesson_detail(request):
    pass


@login_required
def add_lesson(request):
    pass


@login_required
def edit_lesson(request):
    pass


@login_required
def delete_lesson(request):
    pass


@login_required
def mark_list(request):
    pass


@login_required
def edit_marks(request):
    pass
