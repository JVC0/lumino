from django.core.management.base import BaseCommand

from subjects.models import Enrollment, Subject


class Command(BaseCommand):
    help = 'show the average of all subjects'

    def handle(self, *args, **kwargs):
        subjects = Subject.objects.all()
        for subject in subjects:
            print(subject)
            enrollment = Enrollment.objects.filter(subject=subject, mark__isnull=False)
            print(enrollment)

            # if None in subject.enrollments.mark:
            #     continue
            # average = sum(subject.enrollments.mark) / len(subject.enrollments.mark)
            # print(f'{subject.code}: {average}')
