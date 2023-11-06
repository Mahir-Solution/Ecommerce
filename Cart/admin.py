from django.contrib import admin
from .models import Cart_Model,CartItem_Model

class Cart_Admin(admin.ModelAdmin):
    list_display = ['cart_id','date_added']
    
admin.site.register(Cart_Model,Cart_Admin)


class CartItem_Admin(admin.ModelAdmin):
    list_display= ['productfk','cartfk','quantity','is_active']
    list_editable = ('is_active',)
admin.site.register(CartItem_Model,CartItem_Admin)
      
# Register your models here.
