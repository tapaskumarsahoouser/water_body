# Generated by Django 5.0.6 on 2024-08-23 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pond',
            name='sub_location',
        ),
    ]
