# Generated by Django 3.2.3 on 2021-05-25 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0002_badges'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Badges',
            new_name='Badge',
        ),
    ]
