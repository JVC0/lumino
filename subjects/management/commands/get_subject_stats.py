from django.core.management.base import BaseCommand

from subjects.models import Enrollment, Subject



class Command(BaseCommand):
    help = 'show the average of all subjects'

    def handle(self, *args, **kwargs):
        subjects = Subject.objects.all()
        for subject in subjects:
            enrollment = Enrollment.objects.filter(subject=subject, mark__isnull=False).values_list(
                'mark', flat=True
            )
            if len(enrollment) > 0:
                mean = round(sum(enrollment) / len(enrollment), 2)
                print(f'{subject.code}: {mean:.2f}')
