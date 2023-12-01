"""
URL configuration for OnlineShoping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
admin.site.site_header = "Ecommerce Website"
from .views import home
# the below to import for static file image and other all image that we used in our project
from django.conf import settings
from django.conf.urls.static import static
from Product.views import storeview,Searchproduct,product_detail
from Cart.views import cartview,add_cart,removeviewall,remove_item,checkout_view
from Registration.views import register_view,login_view,logout_view,Dashboard_view,activate_view,myorder,change_password
from order.views import place_order,payment,complete_order
from django.urls import include
#from admin_honeypot import views as honeypot_views



urlpatterns = [
    #path('admin/', include('admin_honeypot.urls')),
    # path('admin/', honeypot_views.admin_honeypot, name='admin_honeypot'),
   
    path('wasi_ecommerce/', admin.site.urls),
    path('',home,name='home'),
    path('store/',storeview,name='store'),
    path('category/<slug:category_slug>/',storeview,name="product_by_category"),# here category_slug name can be any that you want same name transfer to given view
    path('search/',Searchproduct,name="search" ),# use for search product
    path('category/<slug:category_slug>/<slug:product_slug>/',product_detail,name="product_detail"),
    path('cart/',cartview,name="cart"),
    path('add_cart/<int:product_id>/',add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_id>/',removeviewall,name='remove'),# this url work to remove button to complete item cart that has one or more item
    path('remove_item/<int:product_id>/<int:cart_id>/',remove_item,name="remove_item"),# this url work on minus button on reduct one item out of all
    path('register/',register_view,name="register"),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('dashboard/',Dashboard_view,name="dashboard"),
    path('activate/<uidb64>/<token>/',activate_view,name="activate"),
    path('checkout/',checkout_view,name="checkout"),
    path('payments/',payment, name = "payments"),
    path('placeorder/',place_order, name = "placeorder"),
    path('ordercomplete/',complete_order, name = "ordercomplete"),
    path('myorder/',myorder,name="myorder"),
    path('change_password/',change_password,name = "change_password"),
    
    
    
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
