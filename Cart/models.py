from django.db import models
from Product.models import Product_Model,Variation_Model
from Registration.models import Registation

class Cart_Model(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)# this cart_id contain session key 
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem_Model(models.Model):
    registrationfk = models.ForeignKey(Registation, on_delete=models.CASCADE,null=True)
    productfk = models.ForeignKey(Product_Model,on_delete=models.CASCADE,null=True)
    variationfk = models.ManyToManyField(Variation_Model,blank=True)
    cartfk = models.ForeignKey(Cart_Model,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.productfk.price* self.quantity
    def __str__(self):
       return self.cartfk.cart_id
    def __str__(self):
       return self.productfk.product_name
# Create your models here.
