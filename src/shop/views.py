from django.shortcuts import render, redirect
from .models import User, Category1, Item, Item_image
from .forms import MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


# Create your views here.

def home(request):
	categories = Category1.objects.exclude(Title='Dress')

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
	context = { 'items':items, 'type':category }
	return render(request, 'shop/list.html', context)


def filter_2_view(request, slug):
	items = Item.objects.filter(category_1__slug=slug)
	category = {}
	if items :
		category = items[0].category_1
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
	context = { 'items':items, 'type':category }
	return render(request, 'shop/list.html', context)


def detail_view(request, pk):
	item = Item.objects.get(id=pk)
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
    return redirect('rooms:room', pk=room.id)


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
