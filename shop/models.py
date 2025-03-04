from django.db import models
from decimal import Decimal
from cloudinary.models import CloudinaryField

class Flower(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = CloudinaryField('image', null=True, blank=True)


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("flower_detail", args=[str(self.id)])
    
class Meta:
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=15, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    address = models.TextField(verbose_name="Адрес доставки")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заказ {self.id} - {self.first_name} {self.last_name}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    flower = models.ForeignKey("Flower", related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return Decimal(self.price) * Decimal(self.quantity)

class PromotionPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    products = models.ManyToManyField("Flower", verbose_name="Товары в акции")
    slug = models.SlugField(unique=True, verbose_name="URL страницы")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("promotion_detail", args=[self.slug])
