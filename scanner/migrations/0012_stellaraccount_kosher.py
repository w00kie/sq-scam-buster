# Generated by Django 3.2.3 on 2021-05-28 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0011_auto_20210526_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='stellaraccount',
            name='kosher',
            field=models.BooleanField(default=False),
        ),
    ]