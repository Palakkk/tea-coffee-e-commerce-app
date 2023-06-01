from django.shortcuts import render,redirect
from django.http import HttpResponse
from app1.models import *
# Create your views here.

def first(request):
    return HttpResponse("<h1>This is my first web page</h1>")

def login(request):
    if request.method == "POST":
        email1=request.POST['email']
        password1=request.POST['password']
        try:
            data=UserRegister.objects.get(email=email1,password=password1)
            if data:
                request.session['email']=data.email
                print(request.session['email'])
                return redirect('index')
            else:
                return render(request,'login.html',{'message':'Invalid email or password'})
        except:
            return render(request,'login.html',{'message':'Invalid email or password'})
    return render(request,'login.html')

def logout(request):
    if 'email' in request.session.keys():
        del request.session['email']
        return redirect('index')
    else:
        return redirect('index')



def table_all(request):
    a=UserRegister.objects.all()
    print("data",a)
    return render(request,'table.html',{"data":a})


def table_filter(request):
    a=UserRegister.objects.filter(email='demo@gmail.com')
    print("data",a)
    return render(request,'table.html',{"data":a})


def table_get(request):
    a=UserRegister.objects.get(email='d@gmail.com')
    print("data",a)
    return render(request,'table_get.html',{"data":a})

def index(request):
    if 'email' in request.session:
        a=request.session['email']
        data=Category.objects.all()
        return render(request,'base.html',{'data':data,'a':a})
    else:
        data=Category.objects.all()
        return render(request,'base.html',{'data':data})

def productall(request):
    if 'email' in request.session:
        a=request.session['email']
        data=Product.objects.all()
        return render(request,'productall.html',{'data':data,'a':a})
    else:
        data=Product.objects.all()
        return render(request,'productall.html',{'data':data})

def productcategorywise(request,id):
    if 'email' in request.session:
        a=request.session['email']
        data=Product.objects.filter(category=id)
        return render(request,'productall.html',{'data':data,'a':a})
    else:
        data=Product.objects.filter(category=id)
        return render(request,'productall.html',{'data':data})  


def singleproduct(request,id):
    if 'email' in request.session:
        a=request.session['email']
        data=Product.objects.get(pk=id)
        return render(request,'singleproduct.html',{'data':data,'a':a})
    else:
        data=Product.objects.get(pk=id)
        return render(request,'singleproduct.html',{'data':data})
    
def register(request):
    if request.method=="POST":
        name1=request.POST['name']
        email1=request.POST['email']
        password1=request.POST['password']
        phone1=request.POST['phone']
        address1=request.POST['address']
        print(name1,email1,password1,address1,phone1)
        data=UserRegister(name=name1,email=email1,password=password1,phone=phone1,address=address1)
        a=UserRegister.objects.filter(email=email1)
        if len(a)==0:
            data.save()
            return redirect('login1')
        else:
            return render(request,'register.html',{'message':"user alredy exist"}) 

    return render(request,'register.html')  
    
def profile(request):
    if 'email' in request.session:
        a=request.session['email']
        user_profile = UserRegister.objects.get(email=a)
        user_orders = Ordermodel.objects.filter(userEmail=a)
        context = {
            'profile': user_profile,
            'orders': user_orders,
            'a':a
        }
        if request.method == 'POST' and 'logout' in request.POST:
            logout(request)
            return redirect('login1')
        else:
            return render(request, 'profile.html', context)
    else:
        return redirect('login1')
    
def myorder(request):
    if 'email' in request.session:
        a = request.session['email']
        user_orders = Ordermodel.objects.filter(userEmail=a)
        prolist=[]
        for i in user_orders:
            pro={}
            productdata=Product.objects.get(id=i.productid)
            pro['img']=productdata.img
            pro['id']=i.productid
            pro['name']=productdata.name
            pro['orderDate']=i.orderDate
            pro['productqty']=i.productqty
            pro['transactionId']=i.transactionId
            pro['paymentMethod']=i.paymentMethod
            pro['orderAmount']=i.orderAmount
            prolist.append(pro)
        return render(request, 'myorder.html', {'a':a, 'prolist':prolist})
        # if user_orders.exists():
        #     context = {
        #         'orders': user_orders,
        #         'a':a
        #     }
        #     return render(request, 'myorder.html', context)
        # else:
        #     return render(request, 'myorder.html', {'message': "No orders placed",'a':a})
    else:
        return redirect('login1')


def changepass(request):
    if 'email' in request.session:
        a=request.session['email']
        user=UserRegister.objects.get(email=a)
        if request.method=="POST":
            old=request.POST['oldpass']
            newpass=request.POST['newpass']
            newpass1=request.POST['newpass1']
            if old==user.password:
                if newpass==newpass1:
                    user.password=newpass
                    user.save()
                    return render(request,'changepass.html',{'message':"New password update",'a':a})
                else:
                    return render(request,'changepass.html',{'message':"New password not match",'a':a})
            else:
                return render(request,'changepass.html',{'message':"Old password not match",'a':a})
            
        return render(request,'changepass.html',{'a':a})
    else:
        return redirect('login1')
    

def contact(request):
    if 'email' in request.session:
        a=request.session['email']
        data=UserRegister.objects.get(email=a)
        if request.method=="POST":
            contact_us=Contactus()
            contact_us.name=request.POST['name']
            contact_us.email=request.POST['email']
            contact_us.phone=request.POST['phone']
            contact_us.message=request.POST['message']
            contact_us.save()
            return render(request,'contactus.html',{'message':"Message Sent Successfully",'a':a})
        return render(request,'contactus.html',{'data':data,'a':a})
    else:
        if request.method=="POST":
            contact_us=Contactus()
            contact_us.name=request.POST['name']
            contact_us.email=request.POST['email']
            contact_us.phone=request.POST['phone']
            contact_us.message=request.POST['message']
            contact_us.save()
            return render(request,'contactus.html',{'message':"Message Sent Successfully"})
        return render(request,'contactus.html')

def feedback(request):
    if 'email' in request.session:
        a=request.session['email']
        data=UserRegister.objects.get(email=a)
        if request.method=="POST":
            fb=Feedback()
            fb.name=request.POST['name']
            fb.email=request.POST['email']
            fb.phone=request.POST['phone']
            fb.feedback=request.POST['feedback']
            fb.save()
            return render(request,'feedback.html',{'message':"Feedback submitted Successfully",'a':a})
        return render(request,'feedback.html',{'data':data,'a':a})
    else:
        if request.method=="POST":
            fb=Feedback()
            fb.name=request.POST['name']
            fb.email=request.POST['email']
            fb.phone=request.POST['phone']
            fb.feedback=request.POST['feedback']
            fb.save()
            return render(request,'feedback.html',{'message':"Feedback submitted Successfully"})
        return render(request,'feedback.html')


import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib import messages
def buynow(request):
    if 'email' in request.session:
        a = UserRegister.objects.get(email=request.session['email'])
        if request.method == "POST":
            product_id = request.POST['id']
            quantity = int(request.POST['quantity'])
            product = Product.objects.get(id=product_id)

            if quantity <= product.quantity:  # Check if requested quantity is available
                request.session['productid'] = product_id
                request.session['quantity'] = quantity
                request.session['userid'] = a.pk
                request.session['username'] = a.name
                request.session['userEmail'] = a.email
                request.session['userContact'] = a.phone
                request.session['address'] = a.address
                request.session['orderAmount'] = product.price * quantity
                request.session['paymentMethod'] = "Razorpay"
                request.session['transactionId'] = ""
                return redirect('razorpayView')
            else:
                messages.error(request, 'Requested quantity exceeds available quantity')
                return redirect(request.META.get('HTTP_REFERER', 'index'))
    else:
        return redirect('login1')

# adding multiple products to cart
# def buynow(request):
#     if 'email' in request.session:
#         a = UserRegister.objects.get(email=request.session['email'])
#         if request.method == "POST":
#             product_id = request.POST['id']
#             quantity = int(request.POST['quantity'])
#             product = Product.objects.get(id=product_id)

#             if quantity <= product.quantity:  # Check if requested quantity is available
#                 cart_item = {
#                     'product_id': product_id,
#                     'quantity': quantity,
#                     'price': product.price
#                 }

#                 if 'cart' not in request.session:
#                     request.session['cart'] = []

#                 request.session['cart'].append(cart_item)
#                 messages.success(request, 'Product added to cart successfully')
#                 request.session.modified = True
#                 return redirect(request.META.get('HTTP_REFERER', 'index'))
#             else:
#                 messages.error(request, 'Requested quantity exceeds available quantity')
#                 return redirect(request.META.get('HTTP_REFERER', 'index'))
#         else:
#             return redirect(request.META.get('HTTP_REFERER', 'index'))
#     else:
#         return redirect('login1')

# def view_cart(request):
#     if 'email' in request.session:
#         a = request.session['email']
#         cart_items = []
        
#         if 'cart' in request.session:
#             for item in request.session['cart']:
#                 product = Product.objects.get(id=item['product_id'])
#                 cart_item = {
#                     'product': product,
#                     'quantity': item['quantity'],
#                     'subtotal': item['quantity'] * item['price']
#                 }
#                 cart_items.append(cart_item)

#         context = {
#             'cart_items': cart_items,
#             'a':a
#         }
#         return render(request, 'cart.html', context=context)
#     else:
#         return redirect('login1')

# def paynow(request):
#     if 'email' in request.session:
#         a = UserRegister.objects.get(email=request.session['email'])
#         cart_items = []        
#         if 'cart' in request.session:
#             total_amount=0
#             for item in request.session['cart']:
#                 product = Product.objects.get(id=item['product_id'])
                
#                 product_id = item['product_id']
#                 quantity = item['quantity']

#                 if quantity <= product.quantity:  # Check if requested quantity is available
#                     total_amount += product.price * quantity
#                 else:
#                     messages.error(request, f"Requested quantity for product {product_id} exceeds available quantity")
#                     return redirect(request.META.get('HTTP_REFERER', 'index'))

#             request.session['productid'] = [item['product_id'] for item in request.session['cart']]
#             request.session['quantity'] = [item['quantity'] for item in request.session['cart']]
#             request.session['userid'] = a.pk
#             request.session['username'] = a.name
#             request.session['userEmail'] = a.email
#             request.session['userContact'] = a.phone
#             request.session['address'] = a.address
#             request.session['orderAmount'] = total_amount
#             request.session['paymentMethod'] = "Razorpay"
#             request.session['transactionId'] = ""
#             return redirect('razorpayView')
#     else:
#         return redirect('login1')


RAZOR_KEY_ID = 'rzp_test_PCLwUnDh0gx1EM'
RAZOR_KEY_SECRET = '5X09bgMznDr8vOIuQ0xCkZ53'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['orderAmount'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['orderAmount'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)

            #Order Save Code
            orderModel = Ordermodel()
            orderModel.productid=request.session['productid']
            orderModel.productqty=request.session['quantity']
            orderModel.userId = request.session['userid']
            orderModel.userName = request.session['username']
            orderModel.userEmail = request.session['userEmail']
            orderModel.userContact = request.session['userContact']
            orderModel.address = request.session['address']
            orderModel.orderAmount = request.session['orderAmount']
            orderModel.paymentMethod = request.session['paymentMethod']
            orderModel.transactionId = payment_id
            productdata=Product.objects.get(id=request.session['productid'])
            productdata.quantity=productdata.quantity-int(request.session['quantity'])
            productdata.save()
            orderModel.save()
            del request.session['productid']
            del request.session['quantity']
            del request.session['userid']
            del request.session['username']
            del request.session['userEmail']
            del request.session['userContact']
            del request.session['address']
            del request.session['orderAmount']
            del request.session['paymentMethod']
            # render success page on successful caputre of payment
            return redirect('orderSuccessView')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello1")
       # if other than POST request is made.
        return HttpResponseBadRequest()

# CART
# def paymenthandler(request):
    # if request.method == "POST":
    #     try:
    #         payment_id = request.POST.get('razorpay_payment_id', '')
    #         razorpay_order_id = request.POST.get('razorpay_order_id', '')
    #         signature = request.POST.get('razorpay_signature', '')

    #         params_dict = {
    #             'razorpay_order_id': razorpay_order_id,
    #             'razorpay_payment_id': payment_id,
    #             'razorpay_signature': signature
    #         }

    #         result = client.utility.verify_payment_signature(params_dict)
            
    #         if result is None:
    #             total_amount = 0
    #             for item in request.session['cart']:
    #                 product = Product.objects.get(id=item['product_id'])
    #                 amount = item['quantity'] * item['price']
    #                 total_amount += amount
    #                 product.quantity -= item['quantity']
    #                 product.save()

    #                 order = Ordermodel(
    #                     productid=item['product_id'],
    #                     productqty=item['quantity'],
    #                     userId=request.session['userid'],
    #                     userName=request.session['username'],
    #                     userEmail=request.session['userEmail'],
    #                     userContact=request.session['userContact'],
    #                     address=request.session['address'],
    #                     orderAmount=amount,
    #                     paymentMethod=request.session['paymentMethod'],
    #                     transactionId=payment_id
    #                 )
    #                 order.save()

    #             del request.session['cart']
    #             del request.session['userid']
    #             del request.session['username']
    #             del request.session['userEmail']
    #             del request.session['userContact']
    #             del request.session['address']
    #             del request.session['paymentMethod']

    #             return redirect('orderSuccessView')
    #         else:
    #             messages.error(request, 'Payment verification failed')
    #             return HttpResponseBadRequest()
    #     except:
    #         messages.error(request, 'An error occurred during payment')
    #         return HttpResponseBadRequest()
    # else:
    #     return HttpResponseBadRequest()

def successview(request):
    if 'email' in request.session:
        a=request.session['email']
        return render(request,'order_sucess.html',{'a':a})
    else:
        return HttpResponseBadRequest()
    
from django.db.models import Q
def searchview(request):
    search_post = request.GET.get('search')
    if search_post:
        posts = Product.objects.filter(Q(category__categoryname__icontains=search_post)|Q(name__icontains=search_post)).distinct()
    else:
        # If not searched, return default posts
        posts = Product.objects.all().order_by("-date_created")
    return render(request,'productall.html',{'data':posts})  

from django.core.mail import send_mail
import random
def forgot(request):
    if request.POST:
        useremail=request.POST['email']
        try:
            data=UserRegister.objects.get(email=useremail)
            otp = random.randint(100000, 999999)
            if data:
                send_mail(
                "Forgot Password",
                "Dear " +str(data.name)+"\n Your OTP is :"+str(otp),
                "youremail",
                [useremail],
                fail_silently=False,
                )
                request.session['otp'] = otp  # Store OTP in session
                return redirect('verify')
                # return render(request, 'verify.html', {'otp': otp,'email':data, 'message':'OTP is sent to your mail'})  # Render the verify.html template with otp
            else:
                return render(request,'forgot.html',{'message':'Email Id Not Found'})
        except:
            return render(request,'forgot.html',{'message':'Email Id Not There'})
    return render(request,'forgot.html')

def verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        otp = request.POST.get('otp')
        if otp == str(request.session.get('otp')):
            print(otp)
            del request.session['otp']
            request.session['email']=email
            print(request.session['email'])
            return redirect('index')
        else:
            return render(request,'verify.html',{'message':'Invalid OTP'})
    
    return render(request, 'verify.html')
