# Generated by Django 4.2.14 on 2024-09-07 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0016_alter_glossarycategory_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glossaryexerciseparameters',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='glossary.glossarycategory'),
        ),
    ]
