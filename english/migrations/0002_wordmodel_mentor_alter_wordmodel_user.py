# Generated by Django 4.2.14 on 2024-08-04 23:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('english', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordmodel',
            name='mentor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mentor_word', to=settings.AUTH_USER_MODEL, verbose_name='Наставник, который добавил слово.'),
        ),
        migrations.AlterField(
            model_name='wordmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_word', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, который изучает слово'),
        ),
    ]