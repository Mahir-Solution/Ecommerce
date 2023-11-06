from django.contrib import admin
from .models import Product_Model,Variation_Model

class PrductAdmin(admin.ModelAdmin):
    list_display = ['product_name','slug','product_image','description','price','stock','is_available']
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('is_available',)


admin.site.register(Product_Model,PrductAdmin)

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['productfkV','variation_category','variation_value','is_active']
    list_filter = ['productfkV','variation_category','variation_value']
    list_editable = ('is_active',)
admin.site.register(Variation_Model,ProductVariationAdmin)

# Register your models here.
