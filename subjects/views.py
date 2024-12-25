from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    AddLessonForm,
    EditLessonForm,
    EditMarkForm,
    EditMarkFormSetHelper,
    EnrollSubjectsForm,
    UnenrollSubjectsForm,
)
from .models import Enrollment, Lesson, Subject
from .tasks import deliver_certificate


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
    return render(request, 'subjects/subject-lessons.html', dict(lessons=lessons, subject=subject))


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
            messages.success(request, 'Lesson was successfully added.')
            return redirect('subjects:lesson-detail', code=subject.code, pk=lesson.pk)
        messages.error(request, messages.ERROR, 'Something went wrong')
    else:
        form = AddLessonForm()
    return render(request, 'subjects/add-lesson.html', {'form': form, 'subject': subject})


@login_required
def edit_lesson(request, code, pk):
    subject = Subject.objects.get(code=code)
    lesson = Lesson.objects.get(id=pk, subject=subject)
    if request.method == 'GET':
        form = EditLessonForm(instance=lesson)
    else:
        form = EditLessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.save()
            messages.success(request, 'Changes were successfully saved.')
            return redirect('subjects:lesson-detail', code=subject.code, pk=lesson.pk)

    return render(
        request, 'subjects/edit-lesson.html', {'form': form, 'lesson': lesson, 'subject': subject}
    )


@login_required
def delete_lesson(request, pk, code):
    lesson = Lesson.objects.get(id=pk)
    messages.success(request, 'Lesson was successfully deleted.')
    lesson.delete()
    return redirect('subjects:subject-detail', code=code)


@login_required
def mark_list(request, code):
    subject = Subject.objects.get(code=code)
    if request.user.profile.is_student() or subject.teacher != request.user:
        return HttpResponseForbidden()
    enrollments = subject.enrollments.all()
    # related_name = 'enrollments' de subject
    return render(
        request, 'subjects/marks/mark-list.html', dict(subject=subject, enrollments=enrollments)
    )


@login_required
def edit_marks(request, code: str):
    subject = Subject.objects.get(code=code)

    MarkFormset = modelformset_factory(Enrollment, form=EditMarkForm, extra=0)
    queryset = subject.enrollments.all()

    if request.method == 'POST':
        formset = MarkFormset(queryset=queryset, data=request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Marks were successfully saved.')
            return redirect(reverse('subjects:mark-list', kwargs={'code': code}))
    else:
        formset = MarkFormset(queryset=queryset)

    helper = EditMarkFormSetHelper()
    return render(
        request,
        'subjects/marks/edit_marks.html',
        {'subject': subject, 'formset': formset, 'helper': helper},
    )


@login_required
def enroll_subjects(request):
    if request.method == 'POST':
        if (form := EnrollSubjectsForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                request.user.enrolled_subjects.add(subject)
                messages.success(request, 'Successfully enrolled in the chosen subjects.')
            return redirect('subjects:subject-list')

    else:
        form = EnrollSubjectsForm(request.user)

    return render(request, 'subjects/enroll.html', dict(form=form))


@login_required
def unenroll_subjects(request):
    if request.method == 'POST':
        if (form := UnenrollSubjectsForm(request.user, data=request.POST)).is_valid():
            subjects = form.cleaned_data['subjects']
            for subject in subjects:
                messages.success(request, 'Successfully unenrolled from the chosen subjects.')
                request.user.enrolled_subjects.remove(subject)
            return redirect('subjects:subject-list')
    else:
        form = UnenrollSubjectsForm(request.user)
    return render(request, 'subjects/unenroll.html', dict(form=form))


@login_required
def request_certificate(request):
    if request.user.enrollments.filter(mark__isnull=False).exists():
        base_url = request.build_absolute_uri('/')
        deliver_certificate.delay(base_url, request.user)
        return render(request, 'subjects/certificate/certificate.html')
    else:
        return HttpResponseForbidden()
