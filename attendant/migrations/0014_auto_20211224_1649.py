# Generated by Django 3.1.6 on 2021-12-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendant', '0013_absent_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absent',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]
