# Generated by Django 4.2.6 on 2023-12-31 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0021_alter_wordmodel_knowledge_assessment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worduserknowledgerelation',
            name='knowledge_assessment',
            field=models.IntegerField(default=0),
        ),
    ]