# Generated by Django 3.1.6 on 2021-12-26 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendant', '0011_auto_20211226_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='StudyField',
        ),
        migrations.AddField(
            model_name='school',
            name='studyfield_code_list',
            field=models.TextField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='studyfield_name_list',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.DeleteModel(
            name='StudyField',
        ),
    ]
