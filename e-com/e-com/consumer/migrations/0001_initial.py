# Generated by Django 5.1.4 on 2025-01-06 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="users",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=200)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
    ]
