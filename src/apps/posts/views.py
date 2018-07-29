from django.shortcuts import render
from .models import Post

from django.http import Http404


def post_list(request):
    posts = Post.objects.active()  # .order_by('-timestamp')
    if request.user.is_staff or request.user.is_superuser:
        posts = Post.objects.all()
    # Se o usuário não tiver autenticado e o post estiver em draft, verá 404
    else:
        raise Http404
    context = {
        'posts': posts,
    }
    return render(request, 'post_list.html', context)
