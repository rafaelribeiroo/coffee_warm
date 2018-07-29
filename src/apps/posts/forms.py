from django import forms
from .models import Post, Tag

from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "iframe_youtube",
        ]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
