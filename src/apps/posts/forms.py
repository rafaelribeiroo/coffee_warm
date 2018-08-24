from django import forms
from .models import Post, Tag, Subscriber

from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Post
        fields = [
            "user",
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
        fields = ['title']  # 'slug'


class SubscriberForm(forms.ModelForm):
    # Define o formulario para os leitores se inscrever no blog
    class Meta:
        model = Subscriber
        fields = ['first_name', 'email_address']


class UnsubscribeForm(forms.Form):
    # Define o formulario para os incritos se desinscreverem
    email_address = forms.EmailField()
