# Generated by Django 4.2.14 on 2025-01-11 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0015_glossaryparams_has_timeout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossaryparams',
            name='count_first',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='glossaryparams',
            name='count_last',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
