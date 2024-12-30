from django.contrib import admin
from .models import Car, Product, CartItem

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price', 'condition')
    list_filter = ('make', 'condition', 'transmission', 'fuel_type')
    search_fields = ('make', 'model', 'description')
    ordering = ('-year',)
    list_per_page = 20

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('stock',)
    ordering = ('name',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__name') 