# Generated by Django 3.1.6 on 2021-12-26 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendant', '0004_remove_school_studyfield_code_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='studyfield_code_list',
            field=models.TextField(blank=True, max_length=220, null=True),
        ),
    ]
