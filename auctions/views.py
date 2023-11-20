from http.client import HTTPResponse
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from urllib import request
from .models import Listing, User, Category, Comments, Bid

# from .forms import Listingform, NameForm


def index(request):
    active_listings = Listing.objects.filter(isActive=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "category": all_categories
    })


def categ(request):
    if request.method == "POST":
        form_category = request.POST['category']
        category = Category.objects.get(categoryName=form_category)
        active_listings = Listing.objects.filter(isActive=True, category=category)
        all_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": active_listings,
            "category": all_categories
        })


def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    is_listing_in_watchlist = request.user in listing_data.wishlist.all()
    is_owner = request.user.username == listing_data.owner.username
    all_comments = Comments.objects.filter(listing == listing_data)
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "is_listing_in_watchlist": is_listing_in_watchlistt,
        "all_comments": all_comments,
        "is_owner": is_owner
    })


def endAuction(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.isActive = False
    listing_data.save()
    is_listing_in_watchlist = request.user in listing_data.wishlist.all()
    is_owner = request.user.username == listing_data.owner.username
    all_comments = Comments.objects.filter(listing=listing_data)
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "is_listing_in_watchlist": is_listing_in_watchlist,
        "all_comments": all_comments,
        "is_owner": is_owner,
        "update": True,
        "message": "Congratulations your action has been closed"

    })


def remove(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.wishlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def add(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.wishlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def watchlist(request):
    current_user = request.user
    listings = current_user.listingWishlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def addcomment(request, id):
    current_user = request.user
    listing_data = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    newComment = Comments(
        author=current_user,
        listing=listing_data,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


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


def create(request):
    #  if this is a POST request we need to process the form data
    if request.method == 'GET':
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "category": all_categories
        })

    else:
        # Get data from page
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        imageUrl = request.POST["imageUrl"]
        category = request.POST["category"]
        # USer
        current_user = request.user
        # Get category listing
        all_categories = Category.objects.all()
        categoryData = Category.objects.get(categoryName=category)
        # Create Newbid
        bid = Bid(bid=int(price), user=current_user)
        bid.save()
        newlisting = Listing(
            title=title,
            description=description,
            price=bid,
            imageUrl=imageUrl,
            category=categoryData,
            owner=current_user,
        )
        # Insert new listing
        newlisting.save()
        # Redirect to new page
        return HttpResponseRedirect(reverse(index))


def addBid(request, id):
    newBid = request.POST["newBid"]
    listing_data = Listing.objects.get(pk=id)
    is_owner = request.user.username == listing_data.owner.username

    if int(newBid) > listing_data.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listing_data.price = updateBid
        listing_data.save()
        # return HttpResponseRedirect(reverse("listing", args=(id, ), kwargs={"message":"Successfull Bid"}))
        return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "message": "Bid Successful",
            "is_owner": is_owner,
            "update": True

        })
    else:
        #  return HttpResponseRedirect(reverse("listing", args=(id, ), kwargs={"message":"Failed Bid"}))
        return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "message": "Bid Failed",
            "update": False,
            "is_owner": is_owner,

        })

        # return HttpResponseRedirect(reverse("listing", args=(id, )))

# def wishlist(request):
#     current_user = request.user
#     listings = current_user.listingWishlist.all()
#     return render(request, "auctions/wishlist.html",{
#         "listings":listings
#     })