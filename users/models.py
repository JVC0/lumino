from django.db import models

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrolled_subjects")
    subject = models.ForeignKey('subjects.Subject', related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateField(auto_now_add=True)
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.student} - {self.subject}'

class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', _('Student')
        TEACHER = 'T', _('Teacher')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles")
    role = models.CharField(max_length=1, choices=Role.choices)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


    def __str__(self):
        return Profile.user
