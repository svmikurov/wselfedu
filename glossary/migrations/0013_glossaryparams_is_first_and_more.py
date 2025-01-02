# Generated by Django 4.2.14 on 2024-12-19 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0012_term_example_term_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='glossaryparams',
            name='is_first',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='glossaryparams',
            name='count_first',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='glossaryparams',
            name='count_last',
            field=models.PositiveSmallIntegerField(default=20),
        ),
    ]
