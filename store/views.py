import requests
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
def store(request):
    products=Paginator(Product.objects.all(),per_page=6)
    page=request.GET.get('page')
    try:
        products=products.page(page)
    except PageNotAnInteger:
        products=products.page(1)
    except EmptyPage:
        products=products.page(products.num_pages)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_total_items
    else:
        items=[]
        order={'get_total_items':0}
        cartItems=order['get_total_items']
    context={'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context=context)
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_total_items
    else:
        items=[]
        order={'get_total_items':0}
        cartItems=order['get_total_items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context=context)
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_total_items
        if request.method=='POST':
            token='5109763905:AAGyxCjkIIZfLMnNAyG10zt5RB_rOKbRPgk'
            # \n abzas
            # \t tab 4 probel
            text=''
            name=request.POST['name']
            email=request.POST['email']
            adress=request.POST['address']
            city=request.POST['city']
            state=request.POST['state']
            zipcode=request.POST['zipcode']
            country=request.POST['country']
            text=f"Xaridor: {name}\n"\
                 f"Email: {email}\n"\
                 f"Adress: {adress}\n"\
                 f"City: {city}\n"\
                 f"Country {country}\n"
            for item in items:
                all=item.product.price* item.quantity
                new=f"Xarid:\t Mahsulot:nomi: {item.product.name} Narxi:{item.product.price}$  Soni: {item.quantity}   Jami: {all}$ "
                text+=new+"\n"
            url=f'https://api.telegram.org/bot{token}/sendMessage?chat_id=1887950744&text={text}'
            
            requests.get(url)
            return redirect('/')
    else:
        items=[]
        order={'get_total_items':0}
        cartItems=order['get_total_items']
    if Customer.objects.filter(user_id=request.user.id).exists():
       customer=Customer.objects.get(user_id=request.user.id)
       context={'items':items,'order':order,'cartItems':cartItems,'customer':customer}
    else:
     context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context=context)
    
def update(request):
    import json
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print(productId,action)
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderitem.quantity=(orderitem.quantity+1)
    elif action=='remove':
        orderitem.quantity=(orderitem.quantity-1)
    orderitem.save()
    if orderitem.quantity <=0:
        orderitem.delete()
    return JsonResponse('Mahsulot qoshildi',safe=False)
def registerPage(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_total_items
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST['name']
            psw=request.POST['psw']
            psw2=request.POST['psw2']
            email=request.POST['email']

            if User.objects.filter(username=name).exists():
                messages.error(request,"Bu username allaqachon ro'yxatdan o'tilgan")
                return redirect('/register')
            if psw != psw2:
                messages.error(request,"Parollar har xil")
                return redirect('/register')
            new=User.objects.create_user(username=name,password=psw,email=email)
            new.save()
            return redirect('/login')


        items=[]
        order={'get_total_items':0}
        cartItems=order['get_total_items']

    context={'cartItems':cartItems}
    return render(request,'store/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
            customer=request.user.customer
            order,created=Order.objects.get_or_create(customer=customer,complete=False)
            items=order.orderitem_set.all()
            cartItems=order.get_total_items
            return redirect('/')
    else:
        items=[]
        order={'get_total_items':0}
        cartItems=order['get_total_items']
        if request.method == 'POST':
            username = request.POST['name']
            password =request.POST['psw']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                
                messages.error(request,"Parol yoki Username xato")
                return redirect('/login')
             
              

    context={'cartItems':cartItems}
    return render(request,'store/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('/login')
def product_detail(request,id):
    if request.user.is_authenticated:
            customer=request.user.customer
            order,created=Order.objects.get_or_create(customer=customer,complete=False)
            items=order.orderitem_set.all()
            cartItems=order.get_total_items
    else:
        items=[]
        order={'get_total_items':0}
        cartItems=order['get_total_items']
    product=Product.objects.get(id=id)
    context={'product':product,'cartItems':cartItems}
    return render(request,'store/product-detail.html',context)