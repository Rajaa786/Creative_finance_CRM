# Generated by Django 4.0.3 on 2022-11-18 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='system_role',
        ),
    ]
