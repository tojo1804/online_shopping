from django.contrib import admin
from .models import Category,Product,Profile
from django.utils.html import mark_safe
from django.contrib.auth.models import User


from django.urls import path
from django.template.response import TemplateResponse

from django.db.models import Count
from django.utils.html import format_html

admin.site.site_header = 'Tojo shop'
admin.site_title = 'ecommerce_tojo'

admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
	list_display= ('name','price','category','is_sale','sale_price','image_tag')
	search_fields =('name',)
	def image_tag(self,obj):
		if obj.image:
			return mark_safe(f'<img src="{obj.image.url}" width="30" height="30" />')
		return "No Image"
	image_tag.short_description = "Image"

	def get_urls(self):
		urls=super().get_urls()
		custom_urls=[path('stats/',self.admin_site.admin_view(self.stats_view),name='product-stats'),]
		return custom_urls + urls
      	
	def  stats_view(self,request):
		category_data = Product.objects.values('category__name').annotate(total=Count('id'))
		labels=[item['category__name'] for item in category_data]
		data=[item['total'] for item in category_data]
		context=dict(self.admin_site.each_context(request),title="Statistiques des Produits",labels=labels,data=data,)
		return TemplateResponse(request, "admin/product_stats.html", context)
       	
        

admin.site.register(Product,ProductAdmin)
admin.site.register(Profile)

#mix profile info and user info
class ProfileInline(admin.StackedInline):
	model=Profile

#extend user model 
class UserAdmin(admin.ModelAdmin):
	model=User
	field=["username","first_name","last_name","email"]
	inlines = [ProfileInline]

#unregister old way 
admin.site.unregister(User)
admin.site.register(User,UserAdmin)



