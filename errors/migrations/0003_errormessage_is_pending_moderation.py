# Generated by Django 4.2.11 on 2024-08-15 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('errors', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='errormessage',
            name='is_pending_moderation',
            field=models.BooleanField(default=False),
        ),
    ]
