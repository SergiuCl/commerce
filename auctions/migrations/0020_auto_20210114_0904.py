# Generated by Django 3.1.4 on 2021-01-14 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20210113_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='listing_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='username',
        ),
    ]
