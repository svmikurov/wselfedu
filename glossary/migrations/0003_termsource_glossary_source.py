# Generated by Django 4.2.14 on 2024-10-28 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('glossary', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Не более 50 символов.', max_length=50, verbose_name='Источник')),
                ('url', models.URLField(blank=True, max_length=255, null=True, verbose_name='URL-адрес источника')),
                ('description', models.CharField(blank=True, help_text='Не более 100 символов.', max_length=100, verbose_name='Описание')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Источник',
                'verbose_name_plural': 'Источники',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='glossary',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='glossary.termsource', verbose_name='Категория'),
        ),
    ]