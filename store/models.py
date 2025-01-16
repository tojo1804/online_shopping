from django.db import models
import datetime 
from django.contrib.auth.models import User
from django.db.models.signals import post_save



#create customer profile de client
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	date_modified=models.DateTimeField(User,auto_now=True)
	phone=models.CharField(max_length=10,blank=True)
	address=models.CharField(max_length=250,blank=True)
	ville=models.CharField(max_length=250,blank=True)
	old_cart=models.CharField(max_length=250,blank=True,null=True)

	def __str__(self):
		return self.user.username

#creat userprofile by default when user signup 
def create_profile(sender,instance,created,**kwargs):
	if created:
		user_profile=Profile(user=instance)
		user_profile.save()
#automate the profile thing 
post_save.connect(create_profile,sender=User)









 

class Category(models.Model):
	name=models.CharField(max_length=50)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name_plural ='categories'


# all of your Product
class Product(models.Model):
	name=models.CharField(max_length=100)
	price=models.DecimalField(default=0,decimal_places=0,max_digits=7)
	category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
	description=models.CharField(max_length=250,default='',blank=True,null=True)
	image=models.ImageField(upload_to='uploads/product/')
	# add stuff 
	is_sale=models.BooleanField(default=False)
	sale_price=models.DecimalField(default=0,decimal_places=0,max_digits=7)

	def __str__(self):
		return self.name


class Client(models.Model):
	first_name=models.CharField(max_length=250)
	last_name=models.CharField(max_length=250)
	phone=models.CharField(max_length=10)
	email=models.EmailField(max_length=100)
	password=models.CharField(max_length=100)
	def __str__(self):
		return f'{self.first_name} {self.last_name}'
