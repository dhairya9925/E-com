# Generated by Django 5.1.4 on 2025-01-09 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_product_addedon_product_updatedon"),
    ]

    operations = [
        migrations.AddField(
            model_name="orders",
            name="totalItems",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
