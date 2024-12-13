from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Subject(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_subjects',
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='subjects.Enrollment', related_name='enrolled_subjects'
    )

    def __str__(self):
        return f'{self.name} ({self.code})'


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    subject = models.ForeignKey(
        'subjects.Subject', related_name='lessons', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        'subjects.Subject', related_name='enrollments', on_delete=models.CASCADE
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['student__last_name', 'student__first_name']

    def __str__(self):
        return f'{self.student} ({self.subject}) {self.mark}'
