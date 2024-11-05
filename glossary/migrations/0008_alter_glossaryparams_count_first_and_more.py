# Generated by Django 4.2.14 on 2024-11-04 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0007_glossaryparams_count_first_glossaryparams_count_last_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossaryparams',
            name='count_first',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='glossaryparams',
            name='count_last',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]