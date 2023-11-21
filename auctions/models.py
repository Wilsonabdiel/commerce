from time import timezone
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName


class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")


class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidprice")
    imageUrl = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    isActive = models.BooleanField(default=True)
    watchliist = models.ManyToManyField(User, blank=True, related_name="listingWishlist")

    def __str__(self):
        return self.title

    # offer = models.FloatField()
    # date = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="usercomment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingcomment")
    message = models.CharField(max_length=300, null=True)




