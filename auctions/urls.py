from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categ",  views.categ, name="categ"),
    path("listing/<int:id>", views.listing, name="listing" ),
    path("remove/<int:id>", views.remove, name="remove"),
    path("add/<int:id>", views.add, name="add"),
    path("watchlist",views.watchlist, name="wishlist"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("endAuction/<int:id>", views.endAuction, name="endAuction"),
]