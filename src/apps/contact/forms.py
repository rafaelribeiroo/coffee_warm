from django import forms
# from django.core.mail import send_mail

# import settings Isso iria importar apenas os arquivos settings.py
# Já no .conf ele trás os settings.py e também as configurações padrões
# do Django
from django.conf import settings

from .utils import send_mail_template


class Contato(forms.Form):

    name = forms.CharField(label='Nome:', max_length=100, required=True)
    email_address = forms.EmailField(label='Email:', required=True)
    CHOICES = (
        ('Sugestão', 'Sugestão'),
        ('Parceria', 'Parceria'),
    )
    option = forms.CharField(
        label='Opção:',
        required=True,
        widget=forms.Select(choices=CHOICES)
    )
    message = forms.CharField(  # Não tem TextField então é CharField
        label='Mande sua sugestão',
        required=True,
        # Widget é o responsável pela renderização
        widget=forms.Textarea
    )

    def send_mail(self):
        subject = self.cleaned_data['option']
        context = {
            'name': self.cleaned_data['name'],
            'email_address': self.cleaned_data['email_address'],
            'message': self.cleaned_data['message'],
        }
        template_name = 'contact_email.html'
        send_mail_template(
            subject, template_name, context, [settings.DEFAULT_FROM_EMAIL]
        )
