from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.create_listing, name="createListing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("addToWatchlist/<int:listing_id>", views.add_to_watchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<int:listing_id>", views.remove_from_watchlist, name="removeFromWatchlist"),
    path("watchlist", views.user_watchlist, name="watchlist"),
    path("closeAuction/<int:listing_id>", views.close_auction, name="closeAuction"),
    path("closedAuctions", views.closed_auctions, name="closedAuctions"),
    path("closedAuction/<int:listing_id>", views.closed_auction, name="closedAuction"),
    path("myWinnings", views.user_winnings, name="myWinnings"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories")
]
