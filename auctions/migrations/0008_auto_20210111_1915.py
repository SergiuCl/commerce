# Generated by Django 3.1.4 on 2021-01-11 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210111_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.IntegerField(null=True),
        ),
    ]
