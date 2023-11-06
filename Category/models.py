from django.db import models
from django.urls import reverse

class Category_Model(models.Model):
    catname = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    catimage = models.ImageField(upload_to='image')
    description = models.TextField()

    def __str__(self):
        return self.catname
    
    def get_url(self):
        return reverse('product_by_category', args=[self.slug])

    
    
    

# Create your models here.
