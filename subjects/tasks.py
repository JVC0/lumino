import datetime
import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job
from weasyprint import HTML
from subjects.models import Enrollment, Subject

@job
def deliver_certificate(base_url, student):
    subjects = Subject.objects.all()
    subject_marks={}
    for subject in subjects:
        enrollment = Enrollment.objects.filter(subject=subject, mark__isnull=False, student=student).first()
        subject_marks[subject.code] = enrollment.mark
                
    rendered = render_to_string(
        'subjects/certificate/certificate.html',
        {
            'subject_marks':subject_marks,
            'student': student,
            'today': datetime.date.today(),
        },
    )

    output_path = os.path.join(
        settings.CERTIFICATES_DIR, f'{student.username}_grade_certificate.pdf'
    )
    os.makedirs(settings.CERTIFICATES_DIR, exist_ok=True)
    HTML(string=rendered, base_url=base_url).write_pdf(output_path)

    email_body = render_to_string('subjects/certificate/email.md', {'student': student})

    email = EmailMessage(
        subject='Grade Certificate',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[student.email],
    )
    email.content_subtype = 'html'
    email.attach_file(output_path)
    email.send()
