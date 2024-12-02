from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Post


def add_enrollment(request):
    if request.method == 'POST':
        post_title = request.POST.get('post-title')
        post_content = request.POST.get('post-content')
        if post_title and post_content:
            post_slug = slugify(post_title)
            Post.objects.create(title=post_title, content=post_content, slug=post_slug)
            return redirect('posts:post-list')
        else:
            return HttpResponse('Title and content are required!')
    return render(request, 'posts/add_post.html')

    # prohiob
