# Generated by Django 5.2.1 on 2025-06-21 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0003_объявление_избранное"),
    ]

    operations = [
        migrations.AddField(
            model_name="объявление",
            name="просмотры",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
