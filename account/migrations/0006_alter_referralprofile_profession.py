# Generated by Django 4.1.2 on 2022-11-14 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_referralprofile_full_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="referralprofile",
            name="profession",
            field=models.CharField(max_length=200),
        ),
    ]