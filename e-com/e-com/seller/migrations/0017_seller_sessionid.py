# Generated by Django 5.1.4 on 2025-01-16 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0016_remove_seller_sessionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='sessionID',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]
