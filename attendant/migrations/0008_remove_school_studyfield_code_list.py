# Generated by Django 3.1.6 on 2021-12-26 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendant', '0007_delete_studyfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='studyfield_code_list',
        ),
    ]
