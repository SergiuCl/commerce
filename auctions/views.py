from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User, AuctionListing, Bid, Comment, Category


def index(request):

    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })


def listing(request, listing_id):
    item = AuctionListing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": item
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
