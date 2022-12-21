from django.contrib import admin
from .models import Category1, Item, OrderItem, Order, User, Item_image


class Category1Admin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('Title',)}
	

class ItemAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('category_2',)}
	search_fields = ['name', 'category_1', 'category_2']


class Item_imageAdmin(admin.ModelAdmin):
	raw_id_field = ['Item']

# Register your models here.
admin.site.register(Category1, Category1Admin)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Item_image, Item_imageAdmin)

