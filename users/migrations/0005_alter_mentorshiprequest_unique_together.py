# Generated by Django 4.2.14 on 2024-08-03 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_mentorship_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mentorshiprequest',
            unique_together={('from_user', 'to_user')},
        ),
    ]
