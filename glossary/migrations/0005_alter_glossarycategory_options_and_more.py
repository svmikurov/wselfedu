# Generated by Django 4.2.14 on 2024-10-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0004_glossary_updated_at_alter_glossary_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='glossarycategory',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='termsource',
            options={'ordering': ('name',), 'verbose_name': 'Источник', 'verbose_name_plural': 'Источники'},
        ),
        migrations.RemoveField(
            model_name='glossarycategory',
            name='url',
        ),
        migrations.AddField(
            model_name='glossarycategory',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='glossarycategory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='glossarycategory',
            name='name',
            field=models.CharField(help_text='Не более 30 символов.', max_length=30, verbose_name='Наименование категории'),
        ),
    ]
