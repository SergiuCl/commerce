# Generated by Django 3.1.4 on 2021-01-13 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20210113_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedauctions',
            name='winner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
