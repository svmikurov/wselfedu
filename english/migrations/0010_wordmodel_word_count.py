# Generated by Django 4.2.6 on 2023-12-23 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0009_alter_wordmodel_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordmodel',
            name='word_count',
            field=models.CharField(choices=[('NC', 'Любое количество слов'), ('OW', 'Слово'), ('CB', 'Словосочетание'), ('PS', 'Часть предложения'), ('ST', 'Предложение')], default='NC', max_length=2),
        ),
    ]
