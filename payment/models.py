from django.db import models
from django.contrib.auth.models import User 
from store.models import Product
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver 
import datetime
from store.models import Product

class ShippingAdress(models.Model): #addresse de livraison
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	shipping_full_name=models.CharField(max_length=255)
	shipping_email=models.EmailField(max_length=255)
	shipping_addresse=models.CharField(max_length=255,null=True,blank=True)
	shipping_city=models.CharField(max_length=255)
	shipping_zipcode=models.CharField(max_length=255,null=True,blank=True)
	shipping_numberphone=models.CharField(max_length=10,null=True, blank=True)
	

	#dont pluralize addrese
	class Meta:
		# verbose_name_plural = "Shipping Address"
		verbose_name_plural = "Adresse Livraison"


	def __str__(self):
		# return f' Shipping Address -{str(self.id)}'
		return f' Address livraison -{str(self.id)}'

#create order model 
class Order(models.Model):   #commande
	#foreign key 
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	full_name=models.CharField(max_length=250)
	email=models.EmailField(max_length=250)
	shipping_addresse=models.TextField(max_length=15000)
	amount_paid=models.DecimalField(max_digits=7,decimal_places=0)
	date_ordered=models.DateTimeField(auto_now_add=True)
	shipped=models.BooleanField(default=False)
	date_shipped=models.DateTimeField(blank=True,null=True)
	def __str__(self):
		return  f' Commande - {str(self.id)}'


#auto add shipping date
@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender,instance,**kwargs):
	if instance.pk:
		now=datetime.datetime.now()
		obj=sender._default_manager.get(pk=instance.pk)
		if instance.shipped and not obj.shipped:
			instance.date_shipped=now

#create order item  model 
class OrderItem(models.Model):
	#foreign key 
	order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
	product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	quantity=models.PositiveBigIntegerField(default=1)
	price=models.DecimalField(max_digits=7,decimal_places=0)
	def __str__(self):
		return f' order item -{str(self.id)}'