# Generated by Django 5.1.4 on 2025-01-16 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0009_users_sessionid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='sessionID',
            field=models.CharField(max_length=36, null=True),
        ),
    ]
