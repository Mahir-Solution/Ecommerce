from django.shortcuts import render,redirect
from django.http import HttpResponse
from Cart.models import CartItem_Model
from .models import Order,OrderProduct
import datetime
import json
from Product.models import Product_Model

def payment(request):
    # body = json.loads(request.body)
    # order = Order.objects.get(userrfk=request.user, is_ordered=False, order_number=body['orderID'])
    #  # Move the cart items to Order Product table
    # cart_items = CartItem_Model.objects.filter(registrationfk = request.user)

    return render(request,'payment.html')

def place_order(request):
    
    # he below code get product on the base of user emial and then count if count less than 0 then redirect to sotre and buy something
    cart_item = CartItem_Model.objects.filter(registrationfk = request.user)
    cart_count = cart_item.count()
    if cart_count < 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    total =0
    quantity =0
    for item in cart_item:
        total += (item.productfk.price * item.quantity)
        quantity += item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
         data = Order()# create the instance of order mean object of order model
         data.user_rfk = request.user# assign login user to  order
         data.first_name = request.POST.get('first_name')
         data.last_name = request.POST.get('last_name')
         data.email = request.POST.get('email')
         data.phone = request.POST.get('phone_number')
         data.address_line_1 = request.POST.get('address1')
         data.address_line_2 = request.POST.get('address2')
         data.city     = request.POST.get('city')
         data.state    = request.POST.get('province')
         data.country     = request.POST.get('Country')
         data.order_total = grand_total
         data.tax = tax
         data.ip = request.META.get('REMOTE_ADDR')
         data.is_ordered = True
         data.save()# all billing info store in order 
         
        # Generate order number
         yr = int(datetime.date.today().strftime('%Y'))
         dt = int(datetime.date.today().strftime('%d'))
         mt = int(datetime.date.today().strftime('%m'))
         d = datetime.date(yr,mt,dt)
         current_date = d.strftime("%Y%m%d") #20210305
         order_number = current_date + str(data.id)# this line helop create order number with current date and user id
         data.order_number = order_number
         data.save()
         #print(order_number)
         order = Order.objects.get(user_rfk =request.user , is_ordered = True, order_number = order_number )
         #print(order.id,'check id by wasim abbas')
         #print(order,'wasim abbas')
         data = {
                 'order': order,
                 'cart_item': cart_item,
                 'tax':tax,
                 'total':total,
                 'grand_total':grand_total,
                 

         }
         
         for item in cart_item:
            #print(item,'wasi rajput')
            orderproduct = OrderProduct()
            orderproduct.order_fk_id= order.id
            #orderproduct.payment_fk = 
            orderproduct.user_rfk_id = request.user.id
            orderproduct.product_fk_id = item.productfk.id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.productfk.price
            orderproduct.ordered = True
            orderproduct.save()
            items = CartItem_Model.objects.get(id=item.id)
            product_variation = items.variationfk.all()
            orderproduct = OrderProduct.objects.get(id = orderproduct.id) 
            orderproduct.variations_fk.set(product_variation)
            orderproduct.save()
         print(product_variation, 'by professor wasim abbas')   
         return render(request,'payment.html',data)
    else:
        return redirect('store')
    
def complete_order(request):
    #first reduct stock and cart empty then show the invoice
    total = 0
    tax = 0
    grand_total = 0
    cart_items = CartItem_Model.objects.filter(registrationfk = request.user)
    for item in cart_items:
        product = Product_Model.objects.get(id=item.productfk_id)
        product.stock -= item.quantity# this line reduce the stock
        product.save()
        total += item.productfk.price * item.quantity
    tax = total *2/100
    grand_total = total+tax
    order = Order.objects.filter(user_rfk = request.user)
    
    justname = CartItem_Model.objects.filter(registrationfk = request.user).first()# tis is used to get only one record becuase in templte i need frist name only once
         
    data = {
        'cart_items':cart_items,
        'order':order,
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
        'justname':justname,
            
    }
    
    # Clear cart
    CartItem_Model.objects.filter(registrationfk =request.user).delete()# this would delete all item that in cart on the base of login user
        
    return render(request,'ordercomplete.html',data)
    # in this view we manage payment later 

# Create your views here.
