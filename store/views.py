from django.shortcuts import render,redirect,get_object_or_404
from .models import Product ,Category, Profile
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from .forms import CustomUserCreationForm,UpdateUserForm,UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAdress
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import login
from django import forms
import json
from cart.cart import Cart

def home(request):
	products=Product.objects.all()
	return render(request,'home.html',{'products':products})

def product_detail(request,pk):
	product=Product.objects.get(id=pk)
	return render(request,'product_detail.html',{'product':product})

def category_page(request,foo):
	cfoo=foo.replace('-',  ' ') 
	try:
		category=Category.objects.get(name=foo)
		products=Product.objects.filter(category=category)
		return render(request,'category_page.html',{'products':products,'category':category})

	except:
		messages.success(request,("that category doesn't existe"))
		return redirect('home') 

def category_rehetra(request):
	categories=Category.objects.all()
	return render(request,'category_rehetra.html',{"categories":categories})

def search_product(request):
	# determine if they fill the form before searching
	if request.method=='POST':
		searched= request.POST['searched']
		#let querry the product 
		searched=Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		#let test for the null ou tsis n 'inonona'
		if not searched:
			messages.success(request,'sorry, desolé, le produit n existe pas.. essayer encore..na tsy misy')
			return render(request,"search.html",{})
		else:
			return render(request,"search.html",{"searched":searched})
			messages.success(request,'io')

	else:
		return render(request,"search.html",{})

def register_user(request):
	if request.method=='POST':
		form=CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,("vous avez bien créé votre compte..  il faut connecter "))
			return redirect('home')
		else:
			messages.success(request,'tsy mety.avereno')
			
			# return redirect('update_info')

	else:
		form=CustomUserCreationForm()
		
	return render(request,'register.html',{'form':form})

def login_user(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']

		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)

			#do some shoppin cart staff 
			current_user= Profile.objects.get(user__id=request.user.id)
			#get thier saved cart from databse 
			saved_cart=current_user.old_cart
			#convert databse string to python dictionnaary 
			if saved_cart:
				#convert into dictionnary using json 
				converted_cart =json.loads(saved_cart)
				#add the loaded dictionnary tyo our session 
				#gett cart 
				cart =Cart(request)
				#loop thru the cart and add items from the database 
				for key,value in converted_cart.items():
					cart.db_add(product=key,quantity=value)


			messages.success(request,("vous êtes connecté au site de commerce"))
			return redirect('home')

		else:

			messages.success(request,("il y a un erreur.. essayer encore"))
			return redirect('login_user')
	else:
		return render(request ,'login.html',{})

def disconnect(request):
	logout(request)
	messages.success(request,("vous êtes déconnecté et reste visiteur seulement"))
	return redirect('home')

def apropos(request):
	return render(request,'apropos.html',{})


@login_required
def update_user(request):
	if request.method=='POST':
		form =UpdateUserForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request,'utilisateur bien modifier avec succée')
			return redirect('home')
	else:
		form=UpdateUserForm(instance=request.user)
		# messages.success(request,'non modifier')

	return render(request,'update_user.html',{'form':form})


def product_stats(request):
    # Préparer les données pour le graphique
    category_data = Product.objects.values('category__name').annotate(total=Count('id'))
    labels = [item['category__name'] for item in category_data]
    data = [item['total'] for item in category_data]

    # Passer les données au template
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'admin/product_stats.html', context)

# def update_info(request):
# 	if request.user.is_authenticated:
# 		# current_user=Profile.objects.get(user__id=request.user.id)
# 		current_user = get_object_or_404(Profile, user__id=request.user.id)
# 		# shipping_user=ShippingAdress.objects.get(user=request.user.id)
# 		shipping_user, created = ShippingAdress.objects.get_or_create(user=request.user)
		
# 		form= UserInfoForm(request.POST or None,instance=current_user)
# 		shipping_form=ShippingForm(request.POST or None,instance=shipping_user)
		
# 		if form.is_valid() or shipping_form.is_valid():
# 			form.save()
# 			shipping_form.save()
# 			return redirect('home')
# 		return render(request,'update_user_info.html',{"form":form,"shipping_form":shipping_form})
# 	else:
# 		messages.success(request,('error, you must be loged'))
# 		return redirect('home')  



def update_info(request):
    if not request.user.is_authenticated:
        messages.error(request, "Erreur : Vous devez être connecté pour accéder à cette page.")
        return redirect('home')
    # Récupération ou création des instances liées à l'utilisateur
    current_user = get_object_or_404(Profile, user__id=request.user.id)
    shipping_user, created = ShippingAdress.objects.get_or_create(user=request.user)

    # Initialisation des formulaires avec les données POST ou les instances existantes
    form = UserInfoForm(request.POST or None, instance=current_user)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

    if request.method == "POST":
        # Validation des deux formulaires
        if form.is_valid() and shipping_form.is_valid():
            form.save()  # Sauvegarde des données utilisateur
            shipping_form.save()  # Sauvegarde de l'adresse de livraison
            messages.success(request, "Vos informations ont été mises à jour avec succès.")
            return redirect('home')
        else:
            # Afficher les erreurs dans les formulaires
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    return render(request,'update_user_info.html',{"form": form, "shipping_form": shipping_form})




