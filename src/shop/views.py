from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Category1, Item, Item_image, ItemLike, ItemRating, Order, OrderItem
from .forms import MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import CheckoutForm


# Create your views here.

def home(request):
	categories = Category1.objects.exclude(Title='Dress')
	for category in categories:
		category.slug = category.Title.lower()
	if request.user.is_authenticated:
		likes = ItemLike.objects.filter(user=request.user)
		count = likes.count()
		orders = Order.objects.filter(
			costumer = request.user,
			active = True
			)
		counts = 0
		if orders:
			order = orders[0]
			counts = order.items.count()
		context = {'types':categories, 'count':count, 'counts':counts}
	context = {'types':categories}
	return render(request, 'index.html', context)


def login_view(request):
	if request.user.is_authenticated :
		return redirect('shop:home')
	else:
		Page = 'login'
		if request.method == 'POST':
			email = request.POST["email"]
			password = request.POST["password"]

			try:
				user = User.objects.get(email=email)
			except:
				messages.error(request, 'The email does not exists')

			else:
				user = authenticate(request, email=email, password=password)


				if user is not None :
					login(request, user)
					if 'next' in request.POST:
						return redirect(request.POST.get('next'))
					else:
						return redirect('shop:home')
				else :
					messages.error(request, 'The password is not correct.')
		context = {'Page':Page}
		return render(request, 'shop/login.html', context )

@csrf_exempt
def register_view(request):
	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
			login(request, user)
			send_email(user)
			return render(request, 'confirm_template.html')
			# return render(request, 'send.html')
			# return redirect('verification')
	form = MyUserCreationForm()
	context = {'form':form}
	return render(request, 'shop/login.html', context )



def logout_view(request):
	logout(request)
	return redirect('shop:home')

# @csrf_exempt
# def sendEmail(request):
# 	password = request.POST.get('password')
# 	username = request.POST.get('username')
# 	email = request.POST.get('email')
# 	user = get_user_model().objects.create(username=username, password=password, email=email)
# 	send_email(user)
# 	return render(request, 'confirm_template.html')


def filter_view(request, slug):
	items = Item.objects.filter(slug=slug)
	category = items[0].category_2
	for item in items :
		bike = ItemLike.objects.filter(
		Q(user = request.user) & 
		Q(item = item)
		)
		item.like = bool(bike)
	context = { 'items':items, 'type':category }
	return render(request, 'shop/list.html', context)


def filter_2_view(request, slug):
	items = Item.objects.filter(category_1__slug=slug)
	category = {}
	if items :
		category = items[0].category_1
		for item in items :
			bike = ItemLike.objects.filter(
			Q(user = request.user) & 
			Q(item = item)
			)
			item.like = bool(bike)
	context = { 'items':items, 'type':category }
	return render(request, 'shop/list.html', context)


def filter_3_view(request, **kwargs):
	slug = kwargs.get('slug')
	category = kwargs.get('pk')
	items = Item.objects.filter(
		Q(slug=slug)&
		Q(category_1__slug=category))
	if items :
		category = str(slug) + ' ' + str(category)
		for item in items :
			bike = ItemLike.objects.filter(
			Q(user = request.user) & 
			Q(item = item)
			)
			item.like = bool(bike)
	context = { 'items':items, 'type':category }
	return render(request, 'shop/list.html', context)


def filter_4_view(request):
	likes = ItemLike.objects.filter(
		user = request.user) 
	items = []
	for like in likes :
		items.append(like.item)
	if items :
		category = 'LIKED'
		for item in items :
			bike = ItemLike.objects.filter(
			Q(user = request.user) & 
			Q(item = item)
			)
			item.like = bool(bike)
	context = { 'items':items, 'type':category }
	return render(request, 'shop/list.html', context)


def detail_view(request, pk):
	item = Item.objects.get(id=pk)
	score = ItemRating.objects.filter(item=item)
	count = score.count()
	print(count)
	s = 0
	if count > 0 :
		for i in range(count):
			rate = score[i]
			s = s + rate.rate
		rating = float(s)/float(count)
		item.rate = rating
		item.save()
	images = Item_image.objects.filter(Item=item)
	context = {'item':item, 'images':images}
	return render(request, 'shop/detail.html', context)



@login_required(login_url='login')
def item_like(request, pk):
    item = Item.objects.get(id=pk)
    like = ItemLike.objects.filter(
    Q(user = request.user) & 
    Q(item = item)
    ) 
    if not like:
        item_like = ItemLike.objects.create(
            user = request.user,
            item = item)
    else:
        ItemLike.objects.filter(
            Q(user = request.user) & 
            Q(item = item)).delete()  
    return redirect('shop:detail', pk=item.id)


@login_required(login_url='login')
def item_rate(request, pk):
	item = Item.objects.get(id=pk)
	score = ItemRating.objects.filter(
		Q(user = request.user) & 
	    Q(item = item)
	    )
	if request.method == "POST" :
		
		if not score:
			rate = request.POST.get('star') 
			item_rate = ItemRating.objects.create(
				user = request.user,
				item = item,
				rate = int(rate)
				)
		else:
			score = ItemRating.objects.get(
				Q(user = request.user) & 
			    Q(item = item)
			    )
			id = score.id
			score = ItemRating.objects.get(id=id)
			rate = request.POST.get('star')
			print(rate) 
			score.rate = int(rate)
			score.save()
			item = score.item
		return redirect('shop:detail', pk=item.id)
	return render(request, 'shop/star.html' )


def remove_from_cart(request, book_id):
    if request.user.is_authenticated():
        try:
            book = Book.objects.get(pk = book_id)
        except ObjectDoesNotExist:
            pass 
        else:
            cart = Cart.objects.get(user = request.user, active=True)
            cart.remove_from_cart(book_id)
        return redirect('cart')
    else:
        return redirect('index')



@login_required(login_url='login')
def add_to_cart(request, pk):
	item = get_object_or_404(Item, id=pk)
	order_item, created = OrderItem.objects.get_or_create(
		item = item,
		costumer = request.user,
		active = True
		)
	order_qs = Order.objects.filter(costumer=request.user, active=True)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item=item).exists():
			order_item.quantity += 1
			order_item.save()
		else:
			order.items.add(order_item)
			order.total += item.price
			order.save()
			messages.info(request, "This item quantity was updated.")
	else :
		order_date = timezone.now()
		order = Order.objects.create(
			costumer=request.user, 
			order_date = order_date,
			)
		order.items.add(order_item)

	return redirect('shop:detail', pk=item.id)



def filter_5_view(request):
	orders = Order.objects.filter(
		costumer = request.user,
		active = True
		)
	order = []
	if orders.exists():
		order = orders[0] 
		order_items = order.items.all()
	if order_items :
		category = 'ordered'
	for order_item in order_items :
		item = order_item.item
		bike = ItemLike.objects.filter(
			Q(user = request.user) & 
			Q(item = item)
			)
		item.like = bool(bike)
	context = { 'items':order_items, 'type':category, 'order':order }
	return render(request, 'shop/list_2.html', context)



@login_required(login_url='login')
def remove_one_item_from_cart(request, pk):
	print('Hellooo')
	item = get_object_or_404(Item, id=pk)
	order_item = get_object_or_404(OrderItem,
		item = item,
		costumer = request.user,
		active = True
		)
	order_qs = Order.objects.filter(costumer=request.user, active=True)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item=item).exists():
			order_item.quantity -= 1
			order_item.save()
			order.total -= item.price
			order.save()
			if order_item.quantity == 0 :
				order.items.remove(order_item)
				order_item.delete()
			messages.info(request, "This item quantity was updated.")
		else:
			messages.error(request, 'the number of this product in your cart is zero.')
	else :
		messages.error(request, 'the number of this product in your cart is zero.')

	return redirect('shop:detail', pk=item.id)


@login_required(login_url='login')
def remove_from_cart(request, pk):
	print('Hellooo')
	item = get_object_or_404(Item, id=pk)
	order_item = get_object_or_404(OrderItem,
		item = item,
		costumer = request.user,
		active = True
		)
	order_qs = Order.objects.filter(costumer=request.user, active=True)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(item=item).exists():
			order.items.remove(order_item)
			order_item.delete()
			messages.info(request, "This set of products was deleted!.")
		else:
			messages.error(request, 'the number of this product in your cart is zero.')
	else :
		messages.error(request, 'the number of this product in your cart is zero.')

	return redirect('shop:detail', pk=item.id)



def OrderSummaryView(request):
    try:
        order = Order.objects.get(costumer=request.user, active=True)
        context = {
            'object': order
        }
        return render(request, 'shop/order_summary.html', context)
    except ObjectDoesNotExist:
        messages.warning(self.request, "You do not have an active order")
        return redirect("shop:home")



def CheckoutView(request):
	try:
		form = CheckoutForm()
		order = Order.objects.get(costumer=request.user, active=True)
		subtotal = order.get_total()
		shipping = 10
		total = subtotal + shipping

		if request.method == 'POST':
			form = forms.CheckoutForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				print('The form is valid.')
				return redirect('shop:checkout')

		context = {'object': order, 'total': total, 'shipping':shipping, 'form':form}
		return render(request, 'shop/checkout.html', context)					
	except ObjectDoesNotExist:
		messages.warning(self.request, "You do not have an active order")
		return redirect("shop:home")
   
