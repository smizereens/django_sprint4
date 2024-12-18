# Generated by Django 3.2.16 on 2024-11-29 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20241129_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст комментария', verbose_name='Текст комментария')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('author', models.ForeignKey(help_text='Выберите автора комментария', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('post', models.ForeignKey(help_text='Выберите публикацию, к которой относится комментарий', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='Публикация')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created_at'],
            },
        ),
    ]
