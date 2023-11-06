from django.shortcuts import render,HttpResponse
from Product.models import Product_Model
from Category.models import Category_Model
from django.db.models import  Q
from django.core.paginator import Paginator
from Cart.models import Cart_Model,CartItem_Model
from Cart.views import _cart_id


def storeview(request,category_slug=None):
    if category_slug != None:# this code work when catgory slug in url and use url path('category/<slug:category_slug>/',storeview,name="product_by_category")
        fetchcategory = Category_Model.objects.get(slug = category_slug)# fetch catgory on the base of slug
        product_context =Product_Model.objects.filter(catgoryfk=fetchcategory,is_available = True).order_by('product_name')# fetch product on the bae of category
        product_count = product_context.count()# count product on the base of product
        if product_context:
            paginator = Paginator(product_context,3)# this line get 3 item out of all item that is comming from database that in in product contect variable
            page =  request.GET.get('page')# this line get current page that use views
            page_product = paginator.get_page(page)# this line show item on page

            product_count = len(page_product)# this line count prodcuct on the base of above line
        else:
            pass
        
        data = {

                'product_context': page_product,
                'product_count':product_count,
               }
        return render(request,"product.html",data)

    else:# the below code work when there is no slug at use the url path('store/',storeview,name='store')
        product_context = Product_Model.objects.all().order_by('product_name')# this line get all product from database
        page_product = 0
        product_count = 0
        if product_context:
            paginator = Paginator(product_context,3)# this line get 3 item out of all item that is comming from database that in in product contect variable
            page =  request.GET.get('page')# this line get current page that use views
            page_product = paginator.get_page(page)# this line show item on page

            product_count = len(page_product)# the len method  count prodcuct on the base of above line page proudct that has value in the form of list
        else:
            pass
        data = {

                'product_context': page_product,
                'product_count':   product_count,
               }
        return render(request,"product.html",data)
# Create your views here.


def Searchproduct(request):
    if 'search_word' in request.GET:
        findword = request.GET['search_word']
        
        if findword:
           product_context = Product_Model.objects.filter((Q(product_name__icontains = findword) & Q(product_name__regex=r'[a-zA-Z]'))  )
           product_count = product_context.count()
        
        Search_data = {
                       'product_context': product_context,
                       'product_count':product_count,
                       
                      }# note here product_context and product acount name must be same as declare in the store view
        #because we render product.html  

        return render(request,"product.html",Search_data)

def product_detail(request,category_slug,product_slug):
    single_product = Product_Model.objects.get(catgoryfk__slug = category_slug, slug = product_slug)
    # catgoryfk_slug then he not use as a slug it get  foreginkey id so we use double undersecore for get slug 
    in_cart = CartItem_Model.objects.filter(cartfk__cart_id = _cart_id(request),productfk = single_product).exists()
    data = {
        'single_product':single_product,
        'in_cart': in_cart,
    }
    #return HttpResponse(single_product)
    return render(request,"product_detail.html",data)