# Generated by Django 4.2.14 on 2024-09-06 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0002_wordmodel_mentor_alter_wordmodel_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('glossary', '0012_rename_email_glossarycategory_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlossaryExerciseSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_start_date', models.CharField(choices=[('DT', 'Сегодня'), ('D3', 'Три дня назад'), ('W1', 'Неделя назад'), ('W2', 'Две недели назад'), ('W3', 'Три недели назад'), ('W4', 'Четыре недели назад'), ('W7', 'Семь недель назад'), ('M3', 'Три месяца назад'), ('M6', 'Шесть месяцев назад'), ('M9', 'Девять месяцев назад'), ('NC', 'Добавлено')])),
                ('period_end_date', models.CharField(choices=[('DT', 'Сегодня'), ('D3', 'Три дня назад'), ('W1', 'Неделя назад'), ('W2', 'Две недели назад'), ('W3', 'Три недели назад'), ('W4', 'Четыре недели назад'), ('W7', 'Семь недель назад'), ('M3', 'Три месяца назад'), ('M6', 'Шесть месяцев назад'), ('M9', 'Девять месяцев назад'), ('NC', 'Добавлено')])),
                ('progres', models.CharField(choices=[('S', 'Изучаю'), ('R', 'Повторяю'), ('E', 'Проверяю'), ('K', 'Знаю')])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='english.categorymodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
