"""ساخت دادهٔ نمونه برای تست سریع APIها.

اجرا:
    python manage.py seed_demo
"""

from decimal import Decimal
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image

from shop.models import (
    Brand,
    Category,
    Comment,
    Customer,
    Product,
    ProductColor,
    ProductImage,
    WishList,
)


def make_image(name, color):
    """یک تصویر ساده PNG در حافظه می‌سازد."""
    buffer = BytesIO()
    Image.new("RGB", (600, 600), color).save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=name)


class Command(BaseCommand):
    help = "ساخت برندها، دسته‌ها، محصولات، مشتری‌ها و دادهٔ نمونه"

    def handle(self, *args, **options):
        brands = {}
        for name in ["Rolex", "Omega", "TAG Heuer"]:
            brands[name], _ = Brand.objects.get_or_create(
                name=name,
                defaults={
                    "meta_title": f"{name} watches",
                    "meta_description": f"لوکس‌ترین ساعت‌های {name}",
                },
            )

        categories = {}
        for title in ["Classic", "Sport", "Diver"]:
            categories[title], _ = Category.objects.get_or_create(title=title)

        products_data = [
            {
                "title": "Rolex Submariner",
                "brand": brands["Rolex"],
                "category": categories["Diver"],
                "price": Decimal("12500.00"),
                "is_luxury": True,
                "is_special": True,
                "gender": "men",
                "origin": "swiss",
                "strap_material": "steel",
                "usage": "diving",
                "design": "classic",
                "engine": "automatic",
                "stash": 3,
                "features": {"water_resistance": "300m", "case": "steel"},
            },
            {
                "title": "Omega Speedmaster",
                "brand": brands["Omega"],
                "category": categories["Sport"],
                "price": Decimal("7800.00"),
                "is_luxury": True,
                "is_special": True,
                "gender": "men",
                "origin": "swiss",
                "strap_material": "leather",
                "usage": "sport",
                "design": "modern",
                "engine": "manual",
                "stash": 5,
                "features": {"water_resistance": "50m", "case": "steel"},
            },
            {
                "title": "TAG Heuer Carrera",
                "brand": brands["TAG Heuer"],
                "category": categories["Classic"],
                "price": Decimal("4200.00"),
                "is_luxury": True,
                "is_special": False,
                "gender": "unisex",
                "origin": "swiss",
                "strap_material": "steel",
                "usage": "formal",
                "design": "classic",
                "engine": "automatic",
                "stash": 7,
                "features": {"water_resistance": "100m", "case": "steel"},
            },
            {
                "title": "Omega Seamaster",
                "brand": brands["Omega"],
                "category": categories["Diver"],
                "price": Decimal("5600.00"),
                "is_luxury": True,
                "is_special": True,
                "gender": "men",
                "origin": "swiss",
                "strap_material": "rubber",
                "usage": "diving",
                "design": "modern",
                "engine": "automatic",
                "stash": 2,
                "features": {"water_resistance": "300m", "case": "steel"},
            },
            {
                "title": "Rolex Datejust",
                "brand": brands["Rolex"],
                "category": categories["Classic"],
                "price": Decimal("9800.00"),
                "is_luxury": True,
                "is_special": False,
                "gender": "women",
                "origin": "swiss",
                "strap_material": "gold",
                "usage": "formal",
                "design": "classic",
                "engine": "automatic",
                "stash": 4,
                "features": {"water_resistance": "100m", "case": "gold"},
            },
            {
                "title": "TAG Heuer Aquaracer",
                "brand": brands["TAG Heuer"],
                "category": categories["Sport"],
                "price": Decimal("2300.00"),
                "is_luxury": False,
                "is_special": False,
                "gender": "unisex",
                "origin": "swiss",
                "strap_material": "steel",
                "usage": "sport",
                "design": "modern",
                "engine": "quartz",
                "stash": 10,
                "features": {"water_resistance": "200m", "case": "steel"},
            },
        ]

        products = []
        for data in products_data:
            product, created = Product.objects.get_or_create(
                title=data["title"], defaults=data
            )
            products.append(product)
            if not product.main_image:
                product.main_image.save(
                    f"{product.slug}.png", make_image("watch.png", "#1f2937"), save=True
                )
            if not product.images.exists():
                ProductImage.objects.create(
                    product=product,
                    image=make_image("gallery.png", "#0f766e"),
                )
            ProductColor.objects.get_or_create(
                product=product,
                color="مشکی",
                defaults={"hex_code": "#111827"},
            )
            ProductColor.objects.get_or_create(
                product=product,
                color="نقره‌ای",
                defaults={"hex_code": "#9ca3af"},
            )

        User = get_user_model()
        customer_user, created = User.objects.get_or_create(
            username="customer1",
            defaults={"email": "customer1@example.com"},
        )
        if created:
            customer_user.set_password("pass12345")
            customer_user.save()

        customer, _ = Customer.objects.get_or_create(
            user=customer_user, defaults={"phone_number": "09120000001"}
        )

        for product in products[:2]:
            WishList.objects.get_or_create(customer=customer, product=product)
            Comment.objects.get_or_create(
                customer=customer,
                product=product,
                defaults={"body": "کیفیت فوق‌العاده‌ای دارد."},
            )

        self.stdout.write(self.style.SUCCESS("دادهٔ نمونه ساخته شد."))
        self.stdout.write(f"تعداد محصولات: {Product.objects.count()}")
        self.stdout.write(f"تعداد مشتری‌ها: {Customer.objects.count()}")
        self.stdout.write(f"تعداد علاقه‌مندی‌ها: {WishList.objects.count()}")
