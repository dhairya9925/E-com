# Generated by Django 5.1.4 on 2025-01-07 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("consumer", "0004_alter_users_contact"),
        ("core", "0002_remove_product_productid_product_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="order",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.orders",
            ),
        ),
    ]
