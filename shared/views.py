from django.shortcuts import redirect, render


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        redirect('subjects:subject-list')
    return render(request, 'homepage.html')
