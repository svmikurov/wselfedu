# Generated by Django 4.2.6 on 2023-12-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0015_merge_20231231_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worduserknowledgerelation',
            name='knowledge_assessment',
            field=models.DecimalField(decimal_places=0, max_digits=2, null=True),
        ),
    ]