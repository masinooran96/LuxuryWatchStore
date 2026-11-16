"""سریالایزرها = مترجم بین مدل‌های جنگو و JSON."""

from rest_framework import serializers

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


def image_url(request, image):
    """آدرس کامل تصویر را برمی‌گرداند؛ اگر تصویر نباشد None."""
    if not image:
        return None
    url = image.url
    return request.build_absolute_uri(url) if request else url


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image_url"]

    def get_image_url(self, obj):
        return image_url(self.context.get("request"), obj.image)


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ["id", "color", "hex_code"]


class CommentSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source="customer.user.username", read_only=True)
    customer_phone = serializers.CharField(source="customer.phone_number", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "customer_username", "customer_phone", "body", "created_at"]


class ProductListSerializer(serializers.ModelSerializer):
    """خروجی سبک برای لیست محصولات؛ فقط فیلدهای لازم."""

    brand_name = serializers.CharField(source="brand.name", read_only=True)
    category_name = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "brand_name",
            "category_name",
            "is_available",
            "stash",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """خروجی کامل یک محصول همراه تصاویر، رنگ‌ها و کامنت‌ها."""

    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    main_image_url = serializers.SerializerMethodField()
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    origin_display = serializers.CharField(source="get_origin_display", read_only=True)
    strap_material_display = serializers.CharField(
        source="get_strap_material_display", read_only=True
    )
    usage_display = serializers.CharField(source="get_usage_display", read_only=True)
    design_display = serializers.CharField(source="get_design_display", read_only=True)
    engine_display = serializers.CharField(source="get_engine_display", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "brand",
            "category",
            "price",
            "is_discount",
            "is_available",
            "is_special",
            "gender",
            "gender_display",
            "origin",
            "origin_display",
            "strap_material",
            "strap_material_display",
            "usage",
            "usage_display",
            "design",
            "design_display",
            "engine",
            "engine_display",
            "main_image_url",
            "features",
            "is_luxury",
            "description",
            "meta_title",
            "meta_description",
            "stash",
            "click_count",
            "created_at",
            "updated_at",
            "images",
            "colors",
            "comments",
        ]

    def get_main_image_url(self, obj):
        return image_url(self.context.get("request"), obj.main_image)


class LuxurySpecialSerializer(serializers.ModelSerializer):
    """خروجی محصولات ویژه و لوکس."""

    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    strap_material_display = serializers.CharField(
        source="get_strap_material_display", read_only=True
    )
    engine_display = serializers.CharField(source="get_engine_display", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "gender",
            "gender_display",
            "strap_material",
            "strap_material_display",
            "engine",
            "engine_display",
        ]


class WishListProductSerializer(serializers.ModelSerializer):
    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "price", "stash", "main_image_url"]

    def get_main_image_url(self, obj):
        return image_url(self.context.get("request"), obj.main_image)


class WishListCustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Customer
        fields = ["username", "email", "phone_number"]


class WishListSerializer(serializers.ModelSerializer):
    product = WishListProductSerializer(read_only=True)
    customer = WishListCustomerSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = ["id", "product", "customer", "created_at"]
