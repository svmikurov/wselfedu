# Generated by Django 4.2 on 2024-06-13 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0009_alter_glossarycategory_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossary',
            name='interpretation',
            field=models.TextField(blank=True, verbose_name='Толкование'),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='term',
            field=models.CharField(max_length=50, verbose_name='Термин'),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='translate',
            field=models.CharField(blank=True, max_length=50, verbose_name='Перевод'),
        ),
    ]
