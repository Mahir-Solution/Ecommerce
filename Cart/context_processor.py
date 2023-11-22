from .models import CartItem_Model,Cart_Model
from .views import _cart_id 
from django.core.exceptions import ObjectDoesNotExist
def counter(request):# this is a context proessor function that return dictionry this method can be use in any template other wise view is generate for every template
    cartcount =0
    if 'admin' in request.path:
        return {}
    else:
        try: 
            #cart = Cart.objects.filter(cart_id = _cart_id(request)).first()
            cart = Cart_Model.objects.get(cart_id = _cart_id(request))# we can use any line 10,11 which show same result
            if request.user.is_authenticated:
                print('wasim')
                print(request.user)
                cartitems = CartItem_Model.objects.all().filter(registrationfk = request.user)
                print(cartitems)   
            else:
                 cartitems = CartItem_Model.objects.all().filter(cartfk = cart)
            for x in cartitems:
                   cartcount += x.quantity
        except ObjectDoesNotExist:
                cart = Cart_Model.objects.create(cart_id=_cart_id(request))# this line create session when there is no session in database other he give error
                cartcount = 0
    
    return dict({'cartcount':cartcount})# return dictionary to template that use this key 
    


