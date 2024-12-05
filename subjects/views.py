from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import AddLessonForm, EditLessonForm, EnrollSubjectsForm, UnenrollSubjectsForm
from .models import Lesson, Subject


# Create your views here.
@login_required
def subject_list(request):
    if request.user.profile.is_student():
        subjects = request.user.enrolled_subjects.all()
    else:
        subjects = request.user.taught_subjects.all()
    for subject in subjects:
        subject.lesson_count = subject.lessons.count()
        subject.student_count = subject.students.count() 
    
    return render(
        request,
        'subjects/subject-list.html',
        dict(subjects=subjects),
    )


@login_required
def subject_detail(request, code):
    subject = Subject.objects.get(code=code)
    if request.user.profile.is_student():
        if not subject.students.filter(pk=request.user.pk).exists():
            return HttpResponseForbidden('You are not enrolled in this subject')
    else:
        if not subject.teacher == request.user:
            return HttpResponseForbidden('You are not the teacher of this subject')
    lessons = Lesson.objects.filter(subject=subject)
    return render(request, 'subjects/subject-lessons.html', dict(lessons=lessons))


@login_required
def lesson_detail(request, pk, code):
    lesson = Lesson.objects.get(pk=pk)
    return render(request, 'subjects/lesson-detail.html', dict(lesson=lesson))
    # esto seguro es más complejo


@login_required
def add_lesson(request, code):
    subject = Subject.objects.get(code=code)
    if request.user.profile.is_student() or subject.teacher != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = AddLessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.subject = subject
            lesson.save()
            return redirect('subjects:lesson-detail', pk=lesson.pk)
    else:
        form = AddLessonForm()
    return render(request, 'subjects/add-lesson.html', dict(form=form))
    pass


@login_required
def edit_lesson(request, pk):
    lesson = Lesson.objects.get(id=pk)
    if request.method == 'GET':
        form = EditLessonForm(instance=lesson)
    else:
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            return redirect('subjects:subjects-lessons')

    return render(request, 'subjects/edit-lesson.html', dict(lesson=lesson, form=form))


def delete_lesson(request, pk):
    lesson = Lesson.objects.get(id=pk)
    lesson.delete()
    return redirect('subjects:subjects-lessons')


@login_required
def mark_list(request, code):
    subject = Subject.objects.get(code=code)
    if request.user.profile.is_student() or subject.teacher != request.user:
        return HttpResponseForbidden()
    enrollments = subject.enrollments.all()
    # related_name = 'enrollments' de subject
    return render(
        request, 'subjects/mark-list.html', dict(subject=subject, enrollments=enrollments)
    )


@login_required
def edit_marks(request):
    pass


def enroll_subjects(request):
    if request.method == 'POST':
        if (form := EnrollSubjectsForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.add(subject)
            return redirect('subjects:subject-list')

    else:
        form = EnrollSubjectsForm(request.user)

    return render(request, 'subjects/enroll.html', dict(form=form))


def unenroll_subjects(request):
    if request.method == 'POST':
        if (form := UnenrollSubjectsForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.remove(subject)
            return redirect('subjects:subject-list')
    else:
        form = UnenrollSubjectsForm(request.user)
    return render(request, 'subjects/unenroll.html', dict(form=form))
