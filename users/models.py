from django.conf import settings
from django.db import models


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_enrollments'
    )
    subject = models.ForeignKey(
        'subjects.Subject', related_name='enrollments', on_delete=models.CASCADE
    )
    enrolled_at = models.DateField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.student} - {self.subject}'


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'Student'
        TEACHER = 'T', 'Teacher'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profiles'
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=Role.choices, default=Role.STUDENT)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/noavatar.png')

    def is_student(self):
        return self.user.profile.role == Profile.Role.STUDENT
        return self.role == Profile.Role.STUDENT

    def __str__(self):
        return Profile.user
        return f'{self.user.username} - {self.get_role_display()}'
