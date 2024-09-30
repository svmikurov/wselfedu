# Generated by Django 4.2.14 on 2024-09-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_alter_points_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='englishtasksettings',
            name='date_end',
            field=models.CharField(choices=[('DT', 'Сегодня'), ('D3', 'Три дня назад'), ('W1', 'Неделя назад'), ('W2', 'Две недели назад'), ('W3', 'Три недели назад'), ('W4', 'Четыре недели назад'), ('W7', 'Семь недель назад'), ('M3', 'Три месяца назад'), ('M6', 'Шесть месяцев назад'), ('M9', 'Девять месяцев назад'), ('NC', 'Добавлено')], default=('DT', 'Сегодня'), max_length=2, verbose_name='Добавлено до'),
        ),
    ]
