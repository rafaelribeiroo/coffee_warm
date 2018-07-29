from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm

from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from urllib.parse import quote_plus
from django.db import transaction
from django.contrib import messages


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


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # Message Success
        messages.success(request, "Criado com sucesso")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'post_create.html', context)


from django.views.generic import DetailView


class PostDetailView(DetailView):
    template_name = 'post_detail.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        instance = get_object_or_404(Post, slug=slug)
        if instance.created > timezone.now().date() or instance.draft:
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise Http404
        return instance

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        instance = context['object']
        context['share_string'] = quote_plus(instance.content)
        return context
