# Generated by Django 4.0.3 on 2022-12-19 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_remove_salinvestments_investments_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salinvestments',
            name='amount',
        ),
    ]
