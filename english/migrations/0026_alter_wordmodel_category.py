# Generated by Django 4.2.6 on 2024-01-04 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0025_alter_wordmodel_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordmodel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='english.categorymodel', verbose_name='Категория'),
        ),
    ]