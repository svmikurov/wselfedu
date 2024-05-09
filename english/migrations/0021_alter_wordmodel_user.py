# Generated by Django 4.2.6 on 2024-05-09 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('english', '0020_alter_categorymodel_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_word', to=settings.AUTH_USER_MODEL),
        ),
    ]
