from django.http import HttpResponse
from django.shortcuts import render
from Product.models import Product_Model

def home(request):
    AllProduct = Product_Model.objects.all()
    data = {

          'AllProduct': AllProduct
    }
    return render(request, "home.html",data)
    #return HttpResponse('this is my home page')