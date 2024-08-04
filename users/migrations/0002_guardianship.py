# Generated by Django 4.2.14 on 2024-07-31 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guardianship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guardian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guardian', to=settings.AUTH_USER_MODEL)),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ward', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('guardian', 'ward')},
            },
        ),
    ]