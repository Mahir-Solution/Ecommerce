from django.db import models
from Category.models import Category_Model
from django.urls import reverse


class Product_Model(models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    product_image = models.ImageField(upload_to='image')
    description =  models.TextField(blank=True)# this field is optional in form validation they will give not error when use can't enter data in the form
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    cteated_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    catgoryfk = models.ForeignKey(Category_Model,on_delete=models.CASCADE,null=True)# when null true he send value to dataase null
    
    def __str__(self):
        return self.product_name
    def product_get_url(self):
        return reverse('product_detail',args=[self.catgoryfk.slug,self.slug])


variation_category_choice=(
       ('color','color'), 
      ('size', 'size'),
      
)# this is tuple with pair value the first size is human readable and second is the value that in database similarly color also




class VariationManager(models.Manager):
    def color_method(self):
        return super(VariationManager,self).filter(variation_category = 'color',is_active = True)
    def size_method(self):
        return super(VariationManager,self).filter(variation_category = 'size',is_active = True)


class Variation_Model(models.Model):
    productfkV = models.ForeignKey(Product_Model,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=200,choices=variation_category_choice)
    variation_value = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    objects = VariationManager()


    def __str__(self):
        return self.variation_value
# Create your models here.
