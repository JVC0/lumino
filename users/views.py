from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from xhtml2pdf import pisa

from subjects.models import Enrollment

from .forms import EditProfileForm


def user_detail(request, username):
    target_user = User.objects.get(username=username)
    return render(
        request,
        'users/user-detail.html',
        {'target_user': target_user},
    )


def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=profile)).is_valid():
            profile = form.save(commit=False)

            profile.save()
            return redirect('user-detail', request.user)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit-profile.html', dict(profile=profile, form=form))


def request_certificate(request, *args, **kwargs):
    enrollments = Enrollment.objects.filter(student=request.user)
    template_path = 'users/certificado.html'
    context = {'enrollments': enrollments}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# https://xhtml2pdf.readthedocs.io/en/stable/usage.html#using-with-python-standalone


def leave(request):
    user = request.user
    # if request.method in ['POST', 'GET']:
    user.delete()
    return redirect('shared:homepage')
