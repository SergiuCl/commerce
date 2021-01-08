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


class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    bid = models.IntegerField()


class Comment(models.Model):
    comment = models.CharField(max_length=60)