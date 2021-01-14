# Generated by Django 3.1.4 on 2021-01-14 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20210114_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='auction_comment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='auction_comment', to='auctions.auctionlisting'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_comment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]