# Generated by Django 3.1.6 on 2021-11-03 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('input_date', models.DateField(blank=True, null=True)),
                ('parent_mobile', models.CharField(max_length=11)),
            ],
        ),
    ]