from django import forms
from .models import Post, Tag

from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Post
        fields = [
            "title",
            "tag",
            "iframe_youtube",
            "content",
            "image",
            "draft",
            "publish",
        ]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
