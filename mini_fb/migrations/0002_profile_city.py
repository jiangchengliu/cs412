# Generated by Django 4.2.16 on 2024-10-06 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="city",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
