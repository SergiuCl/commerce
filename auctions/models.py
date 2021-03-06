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
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None, related_name="auction")
    user_watchlist = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="user_watchlist")


class ClosedAuctions(models.Model):
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="winner")
    won_auction = models.ForeignKey(AuctionListing, on_delete=models.PROTECT, default=None, related_name="won_auction")
    winning_price = models.IntegerField(null=True)
    winning_date = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="user_bid")
    auction_bid = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None, related_name="auction_bid")
    bid = models.IntegerField()


class Comment(models.Model):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="user_comment")
    auction_comment = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None, related_name="auction_comment")
    comment = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(auto_now_add=True)
