from django.urls import path

from .views import (
    LuxurySpecialView,
    ProductDetailView,
    ProductListView,
    WishListView,
)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("luxury-special/", LuxurySpecialView.as_view(), name="luxury-special"),
    path("me/wishlist/", WishListView.as_view(), name="wishlist"),
]
