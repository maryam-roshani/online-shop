from django.db import models
from django.contrib.auth.models import USER

# Create your models here.
class Category(models.Model):
	Title = models.CharField(max_length=100)


class Item(models.Model):
	name = models.CharField(max_length=100)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) 
	picture = models.ImageField(upload_to='media/products', default='media/products/example.jpg')
	price = models.DecimalField( max_digits=10, decimal_places=2)


class OrderItem(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)


class Order(models.Model):
	costumer = models.ForeignKey(USER, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	date_update = models.DateTimeField(auto_now=True)
	items = models.ManyToManyField(OrderItem, on_delete=models.CASCADE)
	total = models.DecimalField( max_digits=50, decimal_places=2)