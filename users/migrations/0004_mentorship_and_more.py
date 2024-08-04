# Generated by Django 4.2.14 on 2024-08-02 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_remove_points_guardianship'),
        ('users', '0003_guardianshiprequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('mentor', 'student')},
            },
        ),
        migrations.RenameModel(
            old_name='GuardianshipRequest',
            new_name='MentorshipRequest',
        ),
        migrations.DeleteModel(
            name='Guardianship',
        ),
    ]
