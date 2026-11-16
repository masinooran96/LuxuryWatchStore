"""مدل‌های فروشگاه ساعت لوکس.

کل پروژه بر پایهٔ ORM جنگو است. هر مدل جدول خودش را دارد.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


# ─────────────────────────────── پایه‌ها ───────────────────────────────
class BaseModel(models.Model):
    """پایهٔ مشترک همهٔ مدل‌ها: زمان ساخت و زمان آخرین ویرایش."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    class Meta:
        abstract = True


class SluggedMixinModel(models.Model):
    """پایهٔ مشترک مدل‌هایی که slug دارند.

    slug = نسخهٔ آدرسی و یکتای عنوان.
    اگر خالی باشد، خودکار از title یا name ساخته می‌شود.
    """

    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="اسلاگ")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base = getattr(self, "title", None) or getattr(self, "name", "")
            base_slug = slugify(base) or "item"
            candidate = base_slug
            number = 2
            while (
                type(self)
                .objects.filter(slug=candidate)
                .exclude(pk=self.pk)
                .exists()
            ):
                candidate = f"{base_slug}-{number}"
                number += 1
            self.slug = candidate
        super().save(*args, **kwargs)


# ─────────────────────────────── انتخاب‌ها ───────────────────────────────
class Gender(models.TextChoices):
    MEN = "men", "مردانه"
    WOMEN = "women", "زنانه"
    UNISEX = "unisex", "یونیسکس"


class Origin(models.TextChoices):
    SWISS = "swiss", "سوئیس"
    JAPANESE = "japanese", "ژاپن"
    GERMAN = "german", "آلمان"
    OTHER = "other", "سایر"


class StrapMaterial(models.TextChoices):
    LEATHER = "leather", "چرم"
    STEEL = "steel", "فولاد"
    GOLD = "gold", "طلا"
    RUBBER = "rubber", "لاستیک"
    CERAMIC = "ceramic", "سرامیک"


class Usage(models.TextChoices):
    CASUAL = "casual", "روزمره"
    FORMAL = "formal", "رسمی"
    SPORT = "sport", "ورزشی"
    DIVING = "diving", "غواصی"


class Design(models.TextChoices):
    CLASSIC = "classic", "کلاسیک"
    MODERN = "modern", "مدرن"
    VINTAGE = "vintage", "وینتیج"
    SKELETON = "skeleton", "اسکلتی"


class Engine(models.TextChoices):
    AUTOMATIC = "automatic", "اتوماتیک"
    QUARTZ = "quartz", "کوارتز"
    MANUAL = "manual", "دستی"
    SMART = "smart", "هوشمند"


# ─────────────────────────────── مدل‌ها ───────────────────────────────
class Brand(BaseModel):
    name = models.CharField(max_length=120, unique=True, verbose_name="نام برند")
    meta_title = models.CharField(max_length=255, blank=True, verbose_name="عنوان متا")
    meta_description = models.TextField(blank=True, verbose_name="توضیح متا")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(BaseModel, SluggedMixinModel):
    title = models.CharField(max_length=120, unique=True, verbose_name="عنوان دسته")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Product(BaseModel, SluggedMixinModel):
    title = models.CharField(max_length=255, verbose_name="عنوان محصول")
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name="products", verbose_name="برند"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products", verbose_name="دسته"
    )

    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت")
    is_discount = models.BooleanField(default=False, verbose_name="تخفیف دارد")
    is_available = models.BooleanField(default=True, verbose_name="موجود")
    is_special = models.BooleanField(default=False, verbose_name="ویژه")

    gender = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.UNISEX, verbose_name="جنسیت"
    )
    origin = models.CharField(
        max_length=20, choices=Origin.choices, default=Origin.OTHER, verbose_name="کشور سازنده"
    )
    strap_material = models.CharField(
        max_length=20,
        choices=StrapMaterial.choices,
        default=StrapMaterial.LEATHER,
        verbose_name="جنس بند",
    )
    usage = models.CharField(
        max_length=20, choices=Usage.choices, default=Usage.CASUAL, verbose_name="کاربرد"
    )
    design = models.CharField(
        max_length=20, choices=Design.choices, default=Design.CLASSIC, verbose_name="طراحی"
    )
    engine = models.CharField(
        max_length=20, choices=Engine.choices, default=Engine.QUARTZ, verbose_name="موتور"
    )

    main_image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="تصویر اصلی"
    )
    features = models.JSONField(default=dict, blank=True, verbose_name="ویژگی‌ها")
    is_luxury = models.BooleanField(default=False, verbose_name="لوکس")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    meta_title = models.CharField(max_length=255, blank=True, verbose_name="عنوان متا")
    meta_description = models.TextField(blank=True, verbose_name="توضیح متا")
    stash = models.PositiveIntegerField(default=0, verbose_name="موجودی انبار")
    click_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="محصول"
    )
    image = models.ImageField(upload_to="products/gallery/", verbose_name="تصویر")

    def __str__(self):
        return f"تصویر {self.product.title}"


class ProductColor(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="colors", verbose_name="محصول"
    )
    color = models.CharField(max_length=50, verbose_name="نام رنگ")
    hex_code = models.CharField(max_length=7, verbose_name="کد رنگ")

    def __str__(self):
        return f"{self.color} - {self.product.title}"


class Customer(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer", verbose_name="کاربر"
    )
    phone_number = models.CharField(max_length=20, verbose_name="شمارهٔ تماس")

    def __str__(self):
        return self.user.username


class WishList(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="wishlist", verbose_name="مشتری"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlists", verbose_name="محصول"
    )

    class Meta:
        unique_together = ("customer", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer} → {self.product}"


class Comment(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="comments", verbose_name="مشتری"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments", verbose_name="محصول"
    )
    body = models.TextField(verbose_name="متن نظر")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"نظر {self.customer} برای {self.product}"
