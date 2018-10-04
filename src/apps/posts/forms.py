from django import forms
from .models import Post, Tag, Subscriber


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "tag",
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
