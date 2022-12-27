from django import template
from shop.models import Order
from django.db import models


register = template.Library()

@register.filter
def cart_item_count(user):
	if user.is_authenticated:
		qs = Order.objects.filter(costumer=user, active=True)
		if qs.exists():
			return qs[0].items.count()
	return 0