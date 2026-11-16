from django.contrib import admin

from .models import (
    Brand,
    Category,
    Comment,
    Customer,
    Product,
    ProductColor,
    ProductImage,
    WishList,
)

admin.site.site_header = "Luxury Watch Store"
admin.site.site_title = "Luxury Watch Store"
admin.site.index_title = "مدیریت فروشگاه ساعت"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "meta_title", "created_at"]
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "created_at"]
    search_fields = ["title"]
    readonly_fields = ["slug"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "brand",
        "category",
        "price",
        "is_available",
        "is_special",
        "is_luxury",
        "stash",
        "click_count",
    ]
    list_filter = [
        "brand",
        "category",
        "is_available",
        "is_special",
        "is_luxury",
        "gender",
        "engine",
    ]
    search_fields = ["title", "brand__name", "category__title"]
    readonly_fields = ["slug", "click_count", "created_at", "updated_at"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image", "created_at"]
    search_fields = ["product__title"]


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ["product", "color", "hex_code"]
    search_fields = ["product__title", "color"]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "created_at"]
    search_fields = ["user__username", "user__email", "phone_number"]


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["customer", "product", "created_at"]
    search_fields = ["customer__user__username", "product__title"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["customer", "product", "body", "created_at"]
    search_fields = ["customer__user__username", "product__title", "body"]
