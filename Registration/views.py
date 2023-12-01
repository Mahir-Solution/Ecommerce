from django.shortcuts import render,HttpResponse,redirect
from .form import RegistrationForm
from .models import  Registation
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password
from Cart.views import _cart_id
from Cart.models import Cart_Model,CartItem_Model
# the below libraya and pakcge for authenticate user through email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth import authenticate,login
import requests
from order.models import Order,OrderProduct


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            phone_number = form.cleaned_data['phone_number']
            passwords = form.cleaned_data['password']
            password = make_password(passwords)
            user = Registation.objects.create(first_name = first_name, last_name = last_name,username = username,email = email,password = password)
            user.phone_number = phone_number
            user.save()
            
            """current_site = get_current_site(request)
            mail_subject = "for the purpose of activation"
            
            message = render_to_string('Registration_varification.html',
                                       {
                                           'user':user,
                                           'domain':current_site,
                                           'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token':default_token_generator.make_token(user),
                                       })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Registration.'
            message = render_to_string('Registration_varification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()"""
            messages.success(request, "Registration Successfully")
            return redirect('register')
            # cleaned_data is a dictionary this would contain all fields of a form cleaned and validate so he avoid  to contain incorrect data
    else:
        form = RegistrationForm()
    
    data = {
        'form':form,
        }
    return render(request,"register.html",data)



def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        passwords = request.POST['password']
        print(email , passwords)
        userlogin =  authenticate(request, username = email,password = passwords)
        if userlogin is not None:
            # code start the blelow code asign cart item to the login user at the time of login with variation or without variation
            try:
                cart = Cart_Model.objects.get(cart_id = _cart_id(request))# get session through the method of _cart_id(request) that is create in cart app view
                is_cart_exist = CartItem_Model.objects.filter(cartfk = cart).exists()# this line check item is exist in database or not
                if is_cart_exist:
                    cart_item = CartItem_Model.objects.filter(cartfk = cart)# get all cart item with the help of session key 
                    # get variatin by cart id mean session key
                    product_variation_list = []# create list
                    for item in cart_item:
                        variation = item.variationfk.all() # get all variation that exist in cart item model in database base on session key/cartid
                        product_variation_list.append(list(variation))# convert all vartion in list and append in ex var list 
                        #print(product_variation_list)
                    # Get the cart items from the user to access his product variations
                    cart_items = CartItem_Model.objects.filter(registrationfk=userlogin)# this is the cart item that add in cart after lodin and fetch item on the base of user asgin 
                    ex_var_list = []
                    id = []
                    for items in cart_items:
                        existing_variation = items.variationfk .all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id) 
                        #print(ex_var_list)      
                    # this code work when same item with same vaiation exist in cart 
                    print('before login',product_variation_list)
                    print('afterlogin',ex_var_list)
                    for x in product_variation_list:# it has all variation that add in cart before login and fetch variation on the base of session key/card it
                        if x in ex_var_list:# it contain all variation  that add in cart after login and fetch variatiion on the base of user asign to the item
                            print('with variation')
                            index = ex_var_list.index(x)# get index of all item that exist in cart iem in database
                            item_id = id[index] # get item id on the base of index
                            item = CartItem_Model.objects.get(id=item_id)
                            item.quantity += 1
                            item.registrationfk = userlogin# assign user to add item, here user is perform already some item in cart after and before login  and agin add item in cart before and after login                                     
                            item.save()
                        else:
                            cart_ite = CartItem_Model.objects.filter(cartfk = cart)
                            for y in cart_ite:
                                y.registrationfk = userlogin
                                y.save()
            except:
                   pass
                        
            #end code that is used to asign cart item to loginuser
            auth.login(request,userlogin)
            messages.success(request,"you are login")
            # the below code for dynamic redirect page
            url = request.META.get('HTTP_REFERER')# at the time of login he get url from url bar
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                   return redirect('dashboard')
            # end for dynamic redirect page code
            
        else:
            messages.error(request,'InValid user Credential')
            return redirect('login')
        

    return render(request,"login.html")
    
    
@login_required(login_url = 'login')# for login required we import above package
def logout_view(request):
    auth.logout(request)
    messages.success(request,"you are logout")
    return redirect('login')

@login_required(login_url = 'login')
def Dashboard_view(request):
    oder = Order.objects.order_by('created_at').filter(user_rfk_id= request.user.id)
    order_count = oder.count()
    data = {
           'order_count':order_count,
    }
    return render(request,"danshboard.html",data)

def activate_view(request,uidb64,token):
    return HttpResponse('registaration ok')

def myorder(request):
    order = Order.objects.filter(user_rfk = request.user, is_ordered = True).order_by('-created_at')
    data = {
        'order':order
    }
    return render(request,"myorder.html",data)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Registation.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
            
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'change_password.html')
# Create your views here.
