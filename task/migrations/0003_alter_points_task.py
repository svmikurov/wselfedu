# Generated by Django 4.2.14 on 2024-07-31 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_points_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='points',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='task.mathematicalexercise'),
        ),
    ]
