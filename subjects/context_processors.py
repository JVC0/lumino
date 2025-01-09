from subjects.models import Subject


def all_subject(request):
    try:
        return {'subjects': Subject.objects.all()}
    except Subject.DoesNotExist:
        return {}
