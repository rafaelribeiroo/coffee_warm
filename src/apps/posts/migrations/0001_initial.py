# Generated by Django 2.1 on 2018-08-27 03:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import src.apps.posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Título')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='URL do titulo')),
                ('image', models.ImageField(height_field='height_field', upload_to=src.apps.posts.models.RandomFileName('imgs_uploaded'), verbose_name='Imagem', width_field='width_field')),
                ('width_field', models.IntegerField(default=0, verbose_name='Largura da imagem')),
                ('height_field', models.IntegerField(default=0, verbose_name='Altura')),
                ('iframe_youtube', models.CharField(default='ala/ii22', max_length=50, verbose_name='Link do Youtube')),
                ('content', models.TextField(verbose_name='Conteúdo')),
                ('draft', models.BooleanField(default=False, verbose_name='Rascunho')),
                ('read_time', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tempo de leitura')),
                ('publish', models.DateField(default=datetime.date.today, verbose_name='Publicação')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Alteração')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Tempo recorrente')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-timestamp', '-updated'],
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='Primeiro nome')),
                ('email_address', models.EmailField(max_length=254, unique=True, verbose_name='Endereco de e-mail')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Titulo')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL do Titulo')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(related_name='blog', to='posts.Tag', verbose_name='Tag correspondente'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
