# Generated by Django 4.2 on 2024-07-02 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0010_alter_glossary_interpretation_alter_glossary_term_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossary',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Добавлено'),
        ),
    ]
