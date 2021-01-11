from django.contrib import admin

from .models import User, AuctionListing, Bid, Comment, Category, Watchlist, ClosedAuctions

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)
admin.site.register(ClosedAuctions)
