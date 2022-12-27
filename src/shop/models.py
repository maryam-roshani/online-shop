from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password=None):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')

        user = self.model(
        		email=self.normalize_email(email),
        		username=username
        	)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
        		email=self.normalize_email(email),
        		username=username,
        		password=password,
        	)
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
        
class User(AbstractBaseUser):
	email = models.EmailField(verbose_name='Email Address', unique=True, null=True)
	username = models.CharField(max_length=100, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', ]

	objects = CustomUserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True



# Create your models here.
class Category1(models.Model):
    Title = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.Title

CATEGORY2_CHOICES = [
('KIDS', 'Kids'),
('WOMEN', 'Women'),
('MEN', 'Men'),
]

class Item(models.Model):
    name = models.CharField(max_length=100)
    category_1 = models.ForeignKey(Category1, on_delete=models.SET_NULL, null=True) 
    category_2 = models.CharField(max_length=5, choices=CATEGORY2_CHOICES, null=True)
    picture = models.ImageField(upload_to='media/products', default='media/products/example.jpg')
    price = models.FloatField()
    slug = models.SlugField(null=True, blank=True)
    rate = models.FloatField(default=0, null=True, blank=True)
    discount_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Item_image(models.Model):
    Image = models.ImageField(upload_to="images")
    Item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='product_images', blank=True, null=True)
    slug = models.SlugField(max_length=200, null=True)
    
    def __str__(self):
        return f'{self.Item}_{self.id} image'


class ItemLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class ItemRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.FloatField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    costumer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    costumer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(OrderItem)
    total = models.FloatField(default=0.00)
    active = models.BooleanField(default=True)
    order_date = models.DateTimeField(null=True)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

# class Cart(models.Model):
#     user = models.ForeignKey(User)
#     active = models.BooleanField(default=True)
#     order_date = models.DateTimeField(null=True)
#     payment_id = models.CharField(max_length=100, null=True)

#     def __unicode__(self): 
#             return "%s" % (self.user)

#     def add_to_cart(self, book_id):
#         item = Item.objects.get(pk=item_id)
#         try:
#             preexisting_order = BookOrder.objects.get(book=book, cart=self)
#             preexisting_order.quantity += 1
#             preexisting_order.save()
#         except BookOrder.DoesNotExist:
#             new_order = BookOrder.objects.create(
#                 book=book,
#                 cart=self,
#                 quantity=1
#                 )
#             new_order.save()

#             def __unicode__(self):
#                 return "%s" % (self.book_id)


#     def remove_from_cart(self, book_id):
#         book = Book.objects.get(pk=book_id)
#         try:
#             preexisting_order = BookOrder.objects.get(book=book, cart=self)
#             if preexisting_order.quantity > 1:
#                 preexisting_order.quantity -= 1
#                 preexisting_order.save()
#             else:
#                 preexisting_order.delete()
#         except BookOrder.DoesNotExist:
#             pass


