# Generated by Django 4.2 on 2024-06-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=25)),
                ('definition', models.CharField(max_length=250)),
                ('interpretation', models.CharField(max_length=250)),
            ],
        ),
    ]