from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


class AuctionListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="owner")
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    image_link = models.CharField(max_length=64, default=None, blank=True, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name="categories")
    orig_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateField(default=None)

    def __str__(self):
        return f"{self.title}"


class Watchlist(models.Model):
    user_id = models.IntegerField(null=True)
    listing_id = models.IntegerField(null=True)


class ClosedAuctions(models.Model):
    winner_id = models.IntegerField(null=True)
    winner_username = models.CharField(max_length=30, default=None)
    listing_title = models.CharField(max_length=30, default=None)
    winning_price = models.IntegerField(null=True)
    image_link = models.CharField(max_length=64, default=None, blank=True, null=True)
    winning_date = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    user = models.IntegerField(null=True)
    title = models.CharField(max_length=64)
    listing_id = models.IntegerField(null=True)
    bid = models.IntegerField()


class Comment(models.Model):
    user_id = models.IntegerField(null=True)
    username = models.CharField(max_length=30, default=None)
    listing_id = models.IntegerField(null=True)
    comment = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(auto_now_add=True)
