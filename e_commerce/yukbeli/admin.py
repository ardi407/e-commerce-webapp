from django.contrib import admin
from .models import OrderItem, Product, Customer, Order, ShippingAddress


admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(ShippingAddress)


# Register your models here.
