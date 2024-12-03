from django.conf import settings
from django.db import models


class Subject(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taught_subjects'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='users.Enrollment', related_name='enrolled_subjects'
    )

    def __str__(self):
        return self.code


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    subject = models.ForeignKey(
        'subjects.Subject', related_name='lessons', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
