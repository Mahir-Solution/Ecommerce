from django.shortcuts import render,redirect,HttpResponse
from .models import Cart_Model,CartItem_Model
from Product.models import Product_Model,Variation_Model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

def _cart_id(request):# this is private method because it is start from undersecore and create session of a user to add item in cart
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):# this method work when add to card in product detail page click 
    product = Product_Model.objects.get(id = product_id)# fetch produt that enter in cart  on the base of id
    if request.user.is_authenticated:# when user is authenticated the below code with work
        if product:
            
            product_variation_list= []
            if request.method == 'POST':#when data come form form with get or psot method he alway in dictioanry form
                for item in request.POST:
                    key = item
                    value = request.POST[key]
                    #print(key + '  '+ value )
                    try:
                        variation = Variation_Model.objects.get(productfkV= product,variation_category__iexact=key,variation_value__iexact=value)
                        product_variation_list.append(variation)
                        print(product_variation_list)
                    except ObjectDoesNotExist:
                            pass
            
            #the get variation from database code is end here

            #we need two thing to save cart item in databae 1) session key that has cart 2)product that fetch on the base of product id
            is_cart_exist = CartItem_Model.objects.filter(productfk = product,registrationfk = request.user).exists()
            if is_cart_exist:
                    cart_item = CartItem_Model.objects.filter(productfk = product, registrationfk = request.user)
                    print(cart_item)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                            existing_variation = item.variationfk.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                        
                    # this code work when same item with same vaiation exist in cart        
                    if product_variation_list in ex_var_list:
                        # increase the cart item
                        #print('wasim')
                        index = ex_var_list.index(product_variation_list)
                        item_id = id[index]
                        #print(item_id)
                        item = CartItem_Model.objects.get(productfk = product,  id=item_id)
                        item.quantity += 1                                     
                        item.save()
                    else:# this code work when same itme exist but not same variation
                        
                        item = CartItem_Model.objects.create(productfk = product,quantity =1, registrationfk = request.user)
                        if len(product_variation_list) > 0:
                            item.variationfk.clear()
                            item.variationfk.add(*product_variation_list)
                        item.save()
            else:# this sript is work when no such time in cart   
                        
                cart_item = CartItem_Model.objects.create(productfk = product,quantity =1, registrationfk = request.user)
                if len(product_variation_list) > 0:
                    cart_item.variationfk.add(*product_variation_list)
                cart_item.save()
            return redirect('cart')
    else:# if user is not authenticated the below code work 
            if product:
                    product_variation_list= []
                    if request.method == 'POST':#when data come form form with get or psot method he alway in dictioanry form
                        for item in request.POST:
                            key = item
                            value = request.POST[key]
                            #print(key + '  '+ value )
                            try:
                                variation = Variation_Model.objects.get(productfkV= product,variation_category__iexact=key,variation_value__iexact=value)
                                product_variation_list.append(variation)
                                #print(product_variation_list)
                            except ObjectDoesNotExist:
                                  pass
                    
                    #the get variation from database code is end here

                    
                    # save cart mean session key in the database
                    try:
                        cart = Cart_Model.objects.get(cart_id = _cart_id(request))
                    except Cart_Model.DoesNotExist:
                        cart = Cart_Model.objects.create(cart_id = _cart_id(request))
                    cart.save() # the above code save cart id on the base of session key that would helop to add cartitem 
                    # the session key store in database is end here



                    #we need two thing to save cart item in databae 1) session key that has cart 2)product that fetch on the base of product id
                    is_cart_exist = CartItem_Model.objects.filter(productfk = product, cartfk = cart).exists()
                    if is_cart_exist:
                            cart_item = CartItem_Model.objects.filter(productfk = product, cartfk = cart)
                            ex_var_list = []
                            id = []
                            for item in cart_item:
                                    existing_variation = item.variationfk.all()
                                    ex_var_list.append(list(existing_variation))
                                    id.append(item.id)
                                    print(ex_var_list)
                                    print(product_variation_list)
                            # this code work when same item with same vaiation exist in cart        
                            if product_variation_list in ex_var_list:
                                print('wasi rajput with alrady exist product with exist variation')
                                index = ex_var_list.index(product_variation_list)
                                item_id = id[index]
                                print(item_id)
                                item = CartItem_Model.objects.get(productfk = product, id=item_id)
                                item.quantity += 1                                     
                                item.save()
                            else:# this code work when same itme exist but not same variation
                                print('wasi rajput with alrady exist product in cart but different varitaion')
                                item = CartItem_Model.objects.create(productfk = product,quantity =1, cartfk = cart)
                                if len(product_variation_list) > 0:
                                    item.variationfk.clear()
                                    item.variationfk.add(*product_variation_list)
                                item.save()
                    else:# this sript is work when no such time in cart   
                        print('wasi rajput for very first itme in cart')
                        cart_item = CartItem_Model.objects.create(productfk = product,quantity =1, cartfk = cart)
                        if len(product_variation_list) > 0:
                            
                            cart_item.variationfk.add(*product_variation_list)
                        cart_item.save()
                    return redirect('cart')

def cartview(request):
    total=0
    quantity=0
    cartitem = None
    
    if request.user.is_authenticated:# the below line show all cart item that is add in cart before and after login
        cartitem = CartItem_Model.objects.filter(registrationfk = request.user, is_active = True)
        print(cartitem)
    else:# the below line of code show item in cart beofre login
         cart = Cart_Model.objects.get(cart_id = _cart_id(request))
         cartitem = CartItem_Model.objects.filter(cartfk =cart, is_active = True)# this line fethc data on the base of session and show in cart view
        
    if cartitem:
            for x in cartitem:
                total += (x.productfk.price*x.quantity)# this is totol price of all product and its quantiy in a cart
                quantity +=x.quantity
                tax = (total*2)/100
                grand_total = tax+total
    else:
            tax =0
            grand_total =0
    data = {

            'cartitem': cartitem,
            'quantity': quantity,
            'total': total,
            'tax':tax,
            'grand_total':grand_total,
    
    }
    return render(request,"cart.html",data)

def remove_item(request,product_id,cart_id):# this view  remove only one item when click on decrement button in a cart template
    productid = Product_Model.objects.get(id = product_id)
    if request.user.is_authenticated:
         cartitem = CartItem_Model.objects.get(productfk =productid,registrationfk = request.user,id = cart_id)
         
    else:
        cartid = Cart_Model.objects.get(cart_id = _cart_id(request))
        cartitem = CartItem_Model.objects.get(productfk =productid,cartfk = cartid,id = cart_id)
    if cartitem.quantity >1:
        cartitem.quantity -=1
        cartitem.save()
    else:
        cartitem.delete()
    return redirect('cart')

        
def removeviewall(request,product_id,cart_id):# this will work when click on remove buttonproductid = Product_Model.objects.get(id = product_id)
    productid = Product_Model.objects.get(id = product_id)
    if request.user.is_authenticated:
         cartitem = CartItem_Model.objects.get(productfk =productid,registrationfk = request.user,id = cart_id)
         
    else:
        cartid = Cart_Model.objects.get(cart_id = _cart_id(request))
        cartitem = CartItem_Model.objects.get(productfk =productid,cartfk = cartid,id = cart_id)
    cartitem.delete()
    return redirect('cart')
@login_required(login_url='login')
def checkout_view(request):# the blow code is same as cart view both are same purpose
     total=0
     quantity=0
     cartitem = None
     if request.user.is_authenticated:# the below line show all cart item that is add in cart before and after login
        cartitem = CartItem_Model.objects.filter(registrationfk = request.user, is_active = True)
        print(cartitem)
     else:# the below line of code show item in cart beofre login
         cart = Cart_Model.objects.get(cart_id = _cart_id(request))
         cartitem = CartItem_Model.objects.filter(cartfk =cart, is_active = True)# this line fethc data on the base of session and show in cart view
        
    
     if cartitem:
            for x in cartitem:
                total += (x.productfk.price*x.quantity)# this is totol price of all product and its quantiy in a cart
                quantity +=x.quantity
                tax = (total*2)/100
                grand_total = tax+total
     else:
            tax =0
            grand_total =0
     data = {

            'cartitem': cartitem,
            'quantity': quantity,
            'total': total,
            'tax':tax,
            'grand_total':grand_total,
    
    }
     return render(request,"checkout.html",data)
# Create your views here.
