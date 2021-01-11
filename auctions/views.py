from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max, Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
import datetime

from .models import User, AuctionListing, Bid, Comment, Category, Watchlist, ClosedAuctions


# set a global var for auction winner
auction_winner = None


def index(request):

    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })


@login_required(login_url="login")
def listing(request, listing_id):

    other_bids = False
    number_of_bids = 0
    user_has_max = False
    user_is_owner = False

# insert the info from form into the db
    if request.method == "POST":
        global auction_winner
        item = AuctionListing.objects.get(pk=listing_id)
        current_user = request.user
        in_watchlist = Watchlist.objects.filter(listing_id=listing_id).filter(user_id=current_user.id)
        other_users_bid = Bid.objects.filter(listing_id=listing_id).aggregate(Max('bid'))
        user_bid = float(request.POST['placeBid'])
        message = None
        # make sure bid is greater then others
        if other_users_bid['bid__max'] is not None:
            # set other bids to true in order to print the number of bids on the page
            other_bids = True
            if user_bid > other_users_bid['bid__max']:
                user_has_max = True
                # add the item to the object
                new_bid = Bid(user=current_user.id, title=item.title, listing_id=listing_id,
                              bid=user_bid)
                new_bid.save()
                auction_winner = current_user
            else:
                message = "Your bid should be greater then the other"
        else:
            # make sure user bid is greater then the item price
            if user_bid >= item.price:
                # set other bids to true in order to print the number of bids on the page
                other_bids = True
                # add the bid to the object
                new_bid = Bid(user=current_user.id, title=item.title, listing_id=listing_id,
                              bid=user_bid)
                new_bid.save()
            else:
                message = "Your bid should be at least as large as the starting bid"

        # count the number of total bids for current item
        number_of_bids = Bid.objects.all().aggregate(
            count=Count('bid', filter=Q(listing_id=listing_id))
        )
        # check if user owns the auction
        if item.owner == current_user:
            user_is_owner = True
        other_users_bid = Bid.objects.filter(listing_id=listing_id).aggregate(Max('bid'))

        return render(request, "auctions/listing.html", {
            "listing": item,
            "in_watchlist": in_watchlist,
            "message": message,
            "max_bid": other_users_bid['bid__max'],
            "other_bids": other_bids,
            "number_of_bids": number_of_bids['count'],
            "user_has_max": user_has_max,
            "user_is_owner": user_is_owner,
            "current_bid": other_users_bid['bid__max']
        })
    else:
        # if method is get
        current_user = request.user
        # get the item
        item = AuctionListing.objects.get(pk=listing_id)
        # check if item in watchlist to be able to display the correct watchlist button
        in_watchlist = Watchlist.objects.filter(listing_id=listing_id).filter(user_id=current_user.id)
        # count the number of bids for the current item
        number_of_bids = Bid.objects.all().aggregate(
            count=Count('bid', filter=Q(listing_id=listing_id))
        )
        # get the max bid
        other_users_bid = Bid.objects.all().aggregate(Max('bid'))
        # if items not None, set other_bids to true
        if other_users_bid['bid__max'] is not None:
            other_bids = True
        # check if user owns the auction
        if item.owner == current_user:
            user_is_owner = True
        return render(request, "auctions/listing.html", {
            "listing": item,
            "in_watchlist": in_watchlist,
            "other_bids": other_bids,
            "number_of_bids": number_of_bids['count'],
            "user_has_max": user_has_max,
            "user_is_owner": user_is_owner,
            "current_bid": other_users_bid['bid__max']
        })


@login_required(login_url="login")
def add_to_watchlist(request, listing_id):
    # check if item already in list
    current_user = request.user
    check_item = Watchlist.objects.filter(listing_id=listing_id).filter(user_id=current_user.id)

    # if item not in the watchlist, add it
    if not check_item:
        # create a new object of type Watchlist
        watchlist_item = Watchlist(user_id=current_user.id, listing_id=listing_id)
        watchlist_item.save()

    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


@login_required(login_url="login")
def remove_from_watchlist(request, listing_id):
    # check if item already in list
    current_user = request.user
    check_item = Watchlist.objects.filter(listing_id=listing_id).filter(user_id=current_user.id)

    # if item in the list, delete it
    if check_item:
        Watchlist.objects.filter(listing_id=listing_id).filter(user_id=current_user.id).delete()

    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


@login_required(login_url="login")
def close_auction(request, listing_id):
    item = AuctionListing.objects.get(pk=listing_id)
    winning_bid = Bid.objects.filter(listing_id=listing_id).aggregate(Max('bid'))
    current_user = request.user
    # nu merge pt ca eu cand dau close sunt current user si trebuie sa vad cine a licitat maxim
    closed_item = ClosedAuctions(winner_id=auction_winner.id, listing_title=item.title,
                                 winner_username=current_user.username, winning_price=winning_bid['bid__max'],
                                 image_link=item.image_link)
    closed_item.save()
    AuctionListing.objects.filter(pk=listing_id).delete()
    Bid.objects.filter(listing_id=listing_id).delete()
    Watchlist.objects.filter(listing_id=listing_id).delete()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url="login")
def user_watchlist(request):
    current_user = request.user
    # get the watchlist items for the current user
    user_w_items = Watchlist.objects.filter(user_id=current_user.id)
    watchlist_items = []

    # make sure query is not None
    if user_w_items:
        # for each item in user items get the Auction Listing and append it to the array
        for o in user_w_items:
            temp = AuctionListing.objects.get(pk=o.listing_id)
            watchlist_items.append(temp)

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items,
    })


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":

        # get the info from user
        auction_title = request.POST["title"]
        auction_price = float(request.POST["price"])

        # make sure values are entered
        if not auction_title:
            return render(request, "auctions/createListing.html", {
                "message": "Please provide a title."
            })
        elif not auction_price:
            return render(request, "auctions/createListing.html", {
                "message": "Please provide a price."
            })

        # create a new object of type AuctionListing
        auction = AuctionListing()
        # add data to object
        auction.owner = request.user
        auction.title = auction_title
        auction.description = request.POST["description"]
        auction.price = auction_price

        if request.POST["image"]:
            auction.image_link = request.POST["image"]
        else:
            auction.image_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/No_image_3x4.svg/1200px-No_image_3x4.svg.png"

        auction.categories = Category.objects.get(pk=int(request.POST["categories"]))

        auction.last_update = datetime.datetime.now()
        auction.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, "auctions/createListing.html", {
        "categories": Category.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
