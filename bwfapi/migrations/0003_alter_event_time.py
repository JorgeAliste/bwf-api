# Generated by Django 4.0.4 on 2022-04-30 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bwfapi', '0002_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.DateTimeField(),
        ),
    ]