from store.models import Product , Profile
class Cart():
	def __init__(self,request):
		self.session=request.session
		#get the request 
		self.request=request

		# get the current session key if it exist
		cart=self.session.get('session_key')
		 # if the user is new, no session key ! create one
		if 'session_key' not in request.session:
			cart=self.session['session_key']={}
		# make sure that cart is available on all pages of the site
		self.cart=cart
	def db_add(self,product,quantity):
		product_id= str(product)
		product_qty= str(quantity)
		#logic 
		if product_id in self.cart:
			pass 
		else:
			# self.cart[product_id] = {'price':str(product.price)}
			self.cart[product_id] = int(product_qty)

		self.session.modified = True
		#deal with logged in 
		if self.request.user.is_authenticated:
			#get thee current  user product and profile 
			current_user=Profile.objects.filter(user__id=self.request.user.id)
			# convert {'3':1, '2':4} to {"3":1, "2":4}
			carty= str(self.cart)
			carty=carty.replace("\'","\"")
			#save carty to the profile model 
			current_user.update(old_cart=str(carty))


	def add(self,product,quantity):
		product_id= str(product.id)
		product_qty= str(quantity)
		#logic 
		if product_id in self.cart:
			pass 
		else:
			# self.cart[product_id] = {'price':str(product.price)}
			self.cart[product_id] = int(product_qty)

		self.session.modified = True
		#deal with logged in 
		if self.request.user.is_authenticated:
			#get thee current  user product and profile 
			current_user=Profile.objects.filter(user__id=self.request.user.id)
			# convert {'3':1, '2':4} to {"3":1, "2":4}
			carty= str(self.cart)
			carty=carty.replace("\'","\"")
			#save carty to the profile model 
			current_user.update(old_cart=str(carty))



	def cart_total(self):
		#get productsq id
		product_ids=self.cart.keys()
		#look up these key in product database
		products=Product.objects.filter(id__in=product_ids)
		#get quantitiies 
		quantities=self.cart
		#let start counting at zero
		total=0
		for key,value in quantities.items():
			# convert key string into int so we can do math
			key=int(key)
			for product in products:
				if product.id==key:
					if product.is_sale:
						total=total + (product.sale_price * value)
					else:
						total=total + (product.price * value)

		return total  







	def __len__(self):
		return len(self.cart)

	def get_prods(self):
		#get id from cart 
		product_ids=self.cart.keys()
		# use id to look up product in database 
		products=Product.objects.filter(id__in=product_ids)

		return products

	def get_quants(self):
		quantities=self.cart
		return quantities

	def update(self,product,quantity):
		product_id=str(product)
		product_qty=int(quantity)

		ourcart=self.cart
		ourcart[product_id] = product_qty

		self.session.modified = True
		#deal with logged in 
		if self.request.user.is_authenticated:
			#get thee current  user product and profile 
			current_user=Profile.objects.filter(user__id=self.request.user.id)
			# convert {'3':1, '2':4} to {"3":1, "2":4}
			carty= str(self.cart)
			carty=carty.replace("\'","\"")
			#save carty to the profile model 
			current_user.update(old_cart=str(carty))
		thing = self.cart 
		return thing
	
	def delete(self,product):
		product_id=str(product)
		if product_id in self.cart:
			del self.cart[product_id]
		self.session.modified=True
		#deal with logged in 
		if self.request.user.is_authenticated:
			#get thee current  user product and profile 
			current_user=Profile.objects.filter(user__id=self.request.user.id)
			# convert {'3':1, '2':4} to {"3":1, "2":4}
			carty= str(self.cart)
			carty=carty.replace("\'","\"")
			#save carty to the profile model 
			current_user.update(old_cart=str(carty))

