"""ویوها = جایی که درخواست را می‌گیریم و پاسخ JSON می‌سازیم."""

from django.db.models import Avg, F, Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Product, WishList
from .serializers import (
    LuxurySpecialSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    WishListSerializer,
)


class ProductListView(APIView):
    """لیست محصولات به همراه نام برند و دسته‌بندی."""

    permission_classes = [AllowAny]

    def get(self, request):
        products = (
            Product.objects.select_related("brand", "category")
            .only(
                "id",
                "title",
                "slug",
                "price",
                "is_available",
                "stash",
                "brand__name",
                "category__title",
            )
            .all()
        )
        serializer = ProductListSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductDetailView(APIView):
    """جزئیات کامل یک محصول + افزایش بهینهٔ click_count."""

    permission_classes = [AllowAny]

    def get(self, request, slug):
        comments = Comment.objects.select_related("customer__user")
        product = get_object_or_404(
            Product.objects.select_related("brand", "category").prefetch_related(
                "images",
                "colors",
                Prefetch("comments", queryset=comments),
            ),
            slug=slug,
        )

        # افزایش اتمی در دیتابیس؛ نه خواندن در پایتون و نه N+1
        Product.objects.filter(pk=product.pk).update(click_count=F("click_count") + 1)
        product.click_count += 1

        serializer = ProductDetailSerializer(
            product, context={"request": request}
        )
        return Response(serializer.data)


class LuxurySpecialView(APIView):
    """محصولات ویژه و لوکس + میانگین قیمت لوکس‌ها در سطح کوئری."""

    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(
            is_special=True,
            is_luxury=True,
            is_available=True,
        ).select_related("brand", "category")

        average = Product.objects.filter(is_luxury=True).aggregate(
            average_price=Avg("price")
        )["average_price"]

        serializer = LuxurySpecialSerializer(
            products, many=True, context={"request": request}
        )
        return Response(
            {
                "average_luxury_price": average,
                "results": serializer.data,
            }
        )


class WishListView(APIView):
    """لیست علاقه‌مندی‌های کاربر لاگین‌شده."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = WishList.objects.filter(
            customer__user=request.user
        ).select_related("product", "customer__user")
        serializer = WishListSerializer(
            wishlists, many=True, context={"request": request}
        )
        return Response(serializer.data)
