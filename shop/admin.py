from django.contrib import admin
from .models import PromotionPage, Flower

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)

@admin.register(PromotionPage)
class PromotionPageAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("products",) 