# Generated by Django 3.2.3 on 2021-05-26 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0009_rename_create_at_payment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_id',
        ),
    ]
