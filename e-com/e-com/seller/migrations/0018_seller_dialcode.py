# Generated by Django 5.1.4 on 2025-01-16 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0017_seller_sessionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='dialCode',
            field=models.CharField(default=91, max_length=5),
            preserve_default=False,
        ),
    ]
