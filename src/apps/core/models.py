from django.db import models


class Subscriber(models.Model):
    email_address = models.EmailField('E-mail')
    name = models.CharField('Nome', max_length=100, blank=True, null=True)
    active = models.BooleanField('Ativo', default=True, blank=True)
