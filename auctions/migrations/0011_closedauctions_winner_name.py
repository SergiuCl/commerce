# Generated by Django 3.1.4 on 2021-01-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210111_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedauctions',
            name='winner_name',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
