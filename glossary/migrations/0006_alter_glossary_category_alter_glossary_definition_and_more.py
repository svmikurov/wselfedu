# Generated by Django 4.2 on 2024-06-10 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0005_glossary_translate_alter_glossary_definition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossary',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='glossary.glossarycategory', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='definition',
            field=models.CharField(blank=True, max_length=250, verbose_name='Определение'),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='interpretation',
            field=models.CharField(blank=True, max_length=250, verbose_name='Толкование'),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='term',
            field=models.CharField(max_length=25, verbose_name='Термин'),
        ),
        migrations.AlterField(
            model_name='glossary',
            name='translate',
            field=models.CharField(blank=True, max_length=25, verbose_name='Перевод'),
        ),
    ]
