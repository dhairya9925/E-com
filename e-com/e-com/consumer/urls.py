from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("cart", views.cart, name="cart"),
    path("profile", views.profile, name="profile"),
    path("deleteAccount", views.deleteAccount, name="deleteAccount"),
]
