# Generated by Django 4.2.6 on 2023-12-23 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0010_wordmodel_word_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordmodel',
            name='word_count',
            field=models.CharField(choices=[('NC', 'Любое количество слов'), ('OW', 'Слово'), ('CB', 'Словосочетание'), ('PS', 'Часть предложения'), ('ST', 'Предложение')], default='NC', max_length=2, verbose_name='Количество слов'),
        ),
    ]