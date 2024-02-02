from django.contrib import admin
from .models import Product, Order, OrderItem, ShippingAddress, Category, Review

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)
admin.site.register(Review)
