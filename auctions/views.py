from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
# connect to models
from .models import User, AuctionListing

from django.contrib import messages

from . import utils
def index(request):
    return render(request, "auctions/index.html")



@login_required
def create_listing(request):

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = request.POST['starting_bid']
        image_url = request.POST.get('image_url', '')
        category = request.POST['category']

        try:
            starting_bid = float(starting_bid)
        except ValueError:
            messages.error(request, 'Invalid starting bid amount. Please enter a valid number.')
            return render(request, 'auctions/create_listing.html')

        if starting_bid <= 0:
            messages.error(request, 'Starting bid amount cannot be zero or negative.')
            return render(request, 'auctions/create_listing.html')

        # if image_url is not None:
        #     image_url = upload_image_to_s3(image_file, image_name)

        auction_listing = AuctionListing(title=title, description=description, starting_bid=starting_bid,
                                         image_url=image_url, category=category)
        auction_listing.user = request.user
        auction_listing.save()

        messages.success(request, 'Listing created successfully!')
        return redirect('listings')

    else:
        return render(request, 'auctions/create_listing.html')


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
