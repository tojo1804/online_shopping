
from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('product_detail/<int:pk>',views.product_detail,name='product_detail'),
    path('category_page/<str:foo>',views.category_page,name='category_page'),
    path('category_rehetra',views.category_rehetra,name='category_rehetra'),
    path('search_product',views.search_product,name='search_product'),
    path('register_user',views.register_user,name='register_user'),
    path('login/',views.login_user,name="login_user"),
    path('disconnect',views.disconnect,name='disconnect'),
    path('apropos',views.apropos,name='apropos'),
    path('update_user',views.update_user,name="update_user"),
    path('stats',views.product_stats,name="product_stats"),
    path('update_info',views.update_info,name='update_info'),
    
]
