from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Cart, Product, OrderPlaced # importing models.py here
from .forms import CustomerCreationForm, CustomerProfileForm
from django.contrib import messages # use import helps us create msg for successful registerations or logins 
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self, request):
        topwears= Product.objects.filter(category= 'TW')
        bottomwears= Product.objects.filter(category= 'BW')
        mobiles= Product.objects.filter(category= 'M')
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        
        # Check if the product is already in the cart
        item_already_in_cart = Cart.objects.filter(product=product, user=request.user).exists()

        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})


@login_required
def add_to_cart(request):
    user= request.user
    product_id= request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user= request.user
        carts= Cart.objects.filter(user=user)
        amount= 0.0
        shipping_amount= 70.0
        total_amount=0.0 
        cart_product= [p for p in Cart.objects.all() if p.user==user] # this checks if the product user == login user 
        # print(cart_product)
        if cart_product: # if cart_product is not empty
            for p in cart_product:
                tempamount= p.quantity * p.product.discounted_price
                amount += tempamount
                totalamount= amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':carts, 'totalamount':totalamount, 'amount':amount})

        else: # when cart is empty
            return render(request, 'app/emptycart.html')


def plus_cart(request): # conneted to myscript.js
    if request.method=='GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) # to get diff product_id for diff user
        c.quantity += 1 
        c.save()

        amount= 0.0
        shipping_amount= 70.0
        totalamount= 0.0
        cart_product= [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount= p.quantity * p.product.discounted_price
            amount += tempamount
        
        data= {'quantity':c.quantity, 'amount':amount, 'totalamount':amount + shipping_amount} # this data is send to myscript.js 
        return JsonResponse(data)


def minus_cart(request): # conneted to myscript.js
    if request.method=='GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) # to get diff product_id for diff user
        c.quantity -= 1 
        c.save()

        amount= 0.0
        shipping_amount= 70.0
        totalamount= 0.0
        cart_product= [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount= p.quantity * p.product.discounted_price
            amount += tempamount
        
        data= {'quantity':c.quantity, 'amount':amount, 'totalamount':amount+shipping_amount} # this data is send to myscript.js 
        return JsonResponse(data)


def remove_cart(request): # conneted to myscript.js
    if request.method=='GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) # to get diff product_id for diff user 
        c.delete()

        amount= 0.0
        shipping_amount= 70.0
        totalamount= 0.0
        cart_product= [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount= p.quantity * p.product.discounted_price
            amount += tempamount
        
        data= {'amount':amount, 'totalamount':amount+shipping_amount} # this data is send to myscript.js 
        return JsonResponse(data)

def buy_now(request):
    return render(request, 'app/buynow.html')

def profile(request):
    return render(request, 'app/profile.html')

@login_required
def address(request):
    add= Customer.objects.filter(user= request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
    op= OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})


def mobile(request, data=None):
    if data==None:
        mobiles= Product.objects.filter(category= 'M')
    elif data=='Samsung' or data=='Motorola':
        mobiles= Product.objects.filter(category= 'M').filter(brand= data)
    elif data=='below':
        mobiles= Product.objects.filter(category= 'M').filter(discounted_price__lt= 30000) # here __lt= less than
    elif data=='above':
        mobiles= Product.objects.filter(category= 'M').filter(discounted_price__gt= 30000) # here __gt= greater than

    return render(request, 'app/mobile.html', {'mobiles':mobiles})


class CustomerRegisterationView(View):
    def get(self, request):
        form= CustomerCreationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
        form= CustomerCreationForm(request.POST) # POST means that this form is coming with some data in it 
        if form.is_valid():
            messages.success(request, 'Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})
    

@login_required
def checkout(request):
    user= request.user
    add= Customer.objects.filter(user=user)
    cart_items= Cart.objects.filter(user=user)
    amount= 0.0
    shipping_amount= 70.0
    totalamount= 0.0
    cart_product= [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount= p.quantity * p.product.discounted_price
            amount += tempamount 
        totalamount= amount+shipping_amount
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


@login_required # for func we can directly use login_required
def payment_done(request):
    user= request.user
    custid= request.GET.get('custid')
    customer= Customer.objects.get(id=custid)
    cart= Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


@method_decorator(login_required, name="dispatch") # for class, we have to use method_decorators
class ProfileView(View):
    def get(self, request):
        form= CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn btn-primary'}) 
        # here we give 'active': btn..... so that when the profile btn is clicked, the btn color stays blue 

    def post(self, request): # post= means the data we get from user 
        form= CustomerProfileForm(request.POST) # now form holds the user data
        if form.is_valid():
            usr= request.user # request= bcz user data is not in customerprofileform
            name= form.cleaned_data['name']
            locality= form.cleaned_data['locality']
            city= form.cleaned_data['city']
            state= form.cleaned_data['state']
            zipcode= form.cleaned_data['zipcode']
            reg= Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        
        return render(request, 'app/profile.html', {'form':form, 'active':'btn btn-primary'})
    

def search(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    else:
        products = Product.objects.none()
    
    return render(request, 'app/search.html', {'products': products, 'query': query})
