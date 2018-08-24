# Generated by Django 2.0.7 on 2018-08-24 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20180822_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='Primeiro nome')),
                ('email_address', models.EmailField(max_length=254, unique=True, verbose_name='Endereco de e-mail')),
            ],
        ),
    ]