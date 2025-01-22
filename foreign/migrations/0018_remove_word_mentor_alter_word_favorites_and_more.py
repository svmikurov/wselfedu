# Generated by Django 4.2.14 on 2025-01-22 03:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foreign', '0017_alter_translateparams_count_first_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='mentor',
        ),
        migrations.AlterField(
            model_name='word',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='word_favorites', through='foreign.WordFavorites', to=settings.AUTH_USER_MODEL, verbose_name='Является ли слово избранным'),
        ),
        migrations.AlterField(
            model_name='word',
            name='foreign_word',
            field=models.CharField(help_text='Не более 75 символов.', max_length=75, verbose_name='Слово на иностранном'),
        ),
        migrations.AlterField(
            model_name='word',
            name='native_word',
            field=models.CharField(help_text='Не более 75 символов.', max_length=75, verbose_name='Слово на родном'),
        ),
        migrations.AlterField(
            model_name='word',
            name='progress',
            field=models.ManyToManyField(blank=True, related_name='word_knowledge', through='foreign.WordProgress', to=settings.AUTH_USER_MODEL, verbose_name='Прогресс изучения слова'),
        ),
        migrations.AlterField(
            model_name='word',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_word', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, который добавил слово'),
        ),
        migrations.CreateModel(
            name='AssignedWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.ManyToManyField(related_name='assigned_student', to=settings.AUTH_USER_MODEL, verbose_name='Назначено слово студенту')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_word', to='foreign.word', verbose_name='Назначенное слово')),
            ],
            options={
                'verbose_name': 'Назначенное слово для изучения',
                'verbose_name_plural': 'Назначенные слова для изучения',
            },
        ),
    ]
