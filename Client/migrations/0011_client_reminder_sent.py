# Generated by Django 5.0.6 on 2024-07-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0010_client_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='reminder_sent',
            field=models.BooleanField(default=False),
        ),
    ]
