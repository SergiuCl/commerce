# Generated by Django 3.1.4 on 2021-01-14 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20210114_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedauctions',
            name='won_auction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='won_auction', to='auctions.auctionlisting'),
        ),
    ]
