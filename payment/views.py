from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.models import ShippingAdress,Order , OrderItem
from payment.forms import ShippingForm,PaymentForm
from django.contrib import messages
from django.contrib.auth.models import User

from store.models import Product,Profile
import datetime


def orders(request,pk):
	if request.user.is_authenticated and request.user.is_superuser:
		order=Order.objects.get(id=pk)
		#get the orderitem 
		items=OrderItem.objects.filter(order=pk)
		if request.POST:
			status=request.POST['shipping_status']
			#check if true or false
			if status=="true":
				order=Order.objects.filter(id=pk)
				now=datetime.datetime.now()
				order.update(shipped=True,date_shipped=now)
			else:
				order=Order.objects.filter(id=pk)
				order.update(shipped=False)
			messages.success(request,("miova..."))
			return redirect('home')

		return render(request,'payment/orders.html',{'order':order,'items':items})

	else:
		messages.success(request,("Non accées,reserver pour admin only"))
		return redirect('home')





def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders=Order.objects.filter(shipped=False)
		if request.POST:
			status=request.POST['shipping_status']
			#check if true or false
			num=request.POST['num']
			order=Order.objects.filter(id=num)
			now=datetime.datetime.now() 
			order.update(shipped=True,date_shipped=now)
			messages.success(request,('niova kah....ho alefa kah'))
		return render(request,'payment/not_shipped_dash.html',{'orders':orders})

	else:
		messages.success(request,'accées interdit')
		return redirect('home')


def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders=Order.objects.filter(shipped=True)
		if request.POST:
			status=request.POST['shipping_status']
			num=request.POST['num']
			order=Order.objects.filter(id=num)
			now=datetime.datetime.now()
			order.update(shipped=False,date_shipped=now)
			messages.success(request,('commande mijanona'))

		return render(request,'payment/shipped_dash.html',{'orders':orders})
	else:
		messages.success(request,("accées interdit"))
		return redirect('home')
 	
 


def process_order(request):
	if request.POST:
		#get the cart 
		cart=Cart(request)
		cart_products=cart.get_prods
		quantities=cart.get_quants
		totals= cart.cart_total()

		#get the billing info from the last page
		payment_form=PaymentForm(request.POST or None)
		#get shipping session data
		my_shipping=request.session.get('my_shipping')
		#gather user info
		full_name=my_shipping['shipping_full_name']
		email=my_shipping['shipping_email']
		#create shipping adresse from from session info
		shipping_addresse=f"{my_shipping['shipping_addresse']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_numberphone']}"

		amount_paid=totals

		#create an order 


		if request.user.is_authenticated:
			user=request.user 
			#create an order 
			create_order=Order(user=user,full_name=full_name,email=email,shipping_addresse=shipping_addresse,amount_paid=amount_paid)
			create_order.save()


			#add order item 
			#get thez order id
			order_id=create_order.pk
			#get the product info
			for product in cart_products():
				product_id=product.id 
				#get the product price 
				if product.is_sale:
					price =product.sale_price
				else:
					price=product.price 
				#get the quantity 
				for key,value in quantities().items():
					if int(key) == product.id:
						#create an order item 
						create_order_item=OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price)
						create_order_item.save()		

			#let delete our cart after order 
			for key in list(request.session.keys()):
				if key== "session_key":
					#delete the key 
					del request.session[key]

			#delete cart from database old_cart_fields
			current_user=Profile.objects.filter(user__id=request.user.id)
			#delete shopping cart in database 
			current_user.update(old_cart="")
			


 


			messages.success(request,'commande placé')
			return redirect('home')
		else:
			#not logging 
			create_order=Order(full_name=full_name,email=email,shipping_addresse=shipping_addresse,amount_paid=amount_paid)
			create_order.save()

			#add order item 
			#get thez order id
			order_id=create_order.pk
			#get the product info
			for product in cart_products():
				product_id=product.id 
				#get the product price 
				if product.is_sale:
					price =product.sale_price
				else:
					price=product.price 
				#get the quantity 
				for key,value in quantities().items():
					if int(key) == product.id:
						#create an order item 
						create_order_item=OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price)
						create_order_item.save()

			#let delete our cart after order 
			for key in list(request.session.keys()):
				if key== "session_key":
					#delete the key 
					del request.session[key]





			messages.success(request,'commande placé')
			return redirect('home')

	else:
		messages.success(request,'accées interdit')
		return redirect('home')
	# return render(request,'payment/process_order.html',{})


 





def billing_info(request):
	if request.POST:
		#get the cart 
		cart=Cart(request)
		cart_products=cart.get_prods
		quantities=cart.get_quants
		totals= cart.cart_total()

		#create shipping info
		my_shipping=request.POST
		request.session['my_shipping']=my_shipping

		if request.user.is_authenticated:
			#get the billing form
			billing_form=PaymentForm()
			return render(request,'payment/billing_info.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})
		else:
			billing_form=PaymentForm()
			return render(request,'payment/billing_info.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})
			
		
		
	else:
		messages.success(request,"Accés interdit,il faut connecter")
		return redirect('home')

def payment_success(request):
	return render(request,'payment/payment_success.html')

# def checkout(request):
# 	#get the cart 
# 	cart=Cart(request)
# 	cart_products=cart.get_prods
# 	quantities=cart.get_quants
# 	totals= cart.cart_total()
# 	if request.user.is_authenticated:
# 		shipping_user, created = ShippingAdress.objects.get_or_create(user=request.user)
# 		# shipping_user=ShippingAddress.objects.get()
# 		shipping_form=ShippingForm(request.POST or None,instance=shipping_user)
# 		return render(request,'payment/checkout.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
# 	else:
# 		# return render(request,'payment/checkout.html',{"cart_products":cart_products,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
# 		messages.success(request,("il connecter ou creer un nouveau pour avoir accées"))
# 		return redirect('home')
	
def checkout(request):
    # Obtenir le panier
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        # Récupérer ou créer une adresse de livraison pour l'utilisateur connecté
        shipping_user, created = ShippingAdress.objects.get_or_create(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        # Si l'utilisateur n'est pas connecté, utiliser un formulaire vierge
        shipping_form = ShippingForm(request.POST or None)
    
    if request.method == 'POST':
        if shipping_form.is_valid():
            # Sauvegarder les informations de livraison
            shipping_form.save()
            messages.success(request, "Les informations de livraison ont été enregistrées avec succès.")
            return redirect('payment_summary')  # Rediriger vers une étape suivante, si nécessaire
    
    return render(request, 'payment/checkout.html', {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form
    })