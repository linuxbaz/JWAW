# Generated by Django 3.1.6 on 2021-12-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendant', '0012_like_date_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='absent',
            name='sent',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
