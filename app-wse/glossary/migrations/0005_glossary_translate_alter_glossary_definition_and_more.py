# Generated by Django 4.2 on 2024-06-10 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0004_alter_glossary_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='glossary',
            name='translate',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='definition',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='interpretation',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
