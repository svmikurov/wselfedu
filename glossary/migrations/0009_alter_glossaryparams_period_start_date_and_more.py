# Generated by Django 4.2.14 on 2024-11-07 14:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0008_alter_glossaryparams_count_first_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossaryparams',
            name='period_start_date',
            field=models.CharField(choices=[('DT', 'Сегодня'), ('D3', 'Три дня назад'), ('W1', 'Неделя назад'), ('W2', 'Две недели назад'), ('W3', 'Три недели назад'), ('W4', 'Четыре недели назад'), ('W7', 'Семь недель назад'), ('M3', 'Три месяца назад'), ('M6', 'Шесть месяцев назад'), ('M9', 'Девять месяцев назад'), ('NC', 'Добавлено')], default='NC', verbose_name='Добавлено после'),
        ),
        migrations.AlterField(
            model_name='glossaryparams',
            name='progress',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), default=['S'], size=None, verbose_name='Уровень знания'),
        ),
    ]
