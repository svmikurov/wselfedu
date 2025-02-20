# Generated by Django 4.2.14 on 2024-10-25 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foreign', '0003_translateparams_count_first_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translateparams',
            name='count_first',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Количество первых добавленных слов'),
        ),
        migrations.AlterField(
            model_name='translateparams',
            name='count_last',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Количество последних добавленных слов'),
        ),
    ]
