# Generated by Django 5.1.4 on 2025-01-16 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0012_remove_users_sessionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='sessionID',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]
