from django.contrib import admin

from .models import Enrollment, Lesson, Subject


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'mark')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [EnrollmentInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'subject')
