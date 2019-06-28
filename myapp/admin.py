from django.contrib import admin
from django.db.models import F
# Register your models here.
from .models import Category, Product, Client, Order

admin.site.register(Category)
# admin.site.register(Product)
#admin.site.register(Client)
admin.site.register(Order)


def increment_stock(modeladmin, request, queryset):
    # for product in Product.objects.filter(available=True):
    #     product.stock = product.stock + 50
    #     product.save(update_fields=['stock'])
    queryset.update(stock=F('stock')+50)


increment_stock.short_description = 'Increment Stock'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    actions = [increment_stock]


admin.site.register(Product, ProductAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city')


admin.site.register(Client, ClientAdmin)
