from django.shortcuts import get_object_or_404, render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
# Create your views here.



def index(request):
    mobiles=Products.objects.filter(category="smartphone").filter(pro_rating__gte=4.3)[:8]
    laptop=Products.objects.filter(category="laptops").filter(pro_rating__gt=4)[:8]
    return render(request, 'index.html',{"mobiles":mobiles,"laptop":laptop})


def register(request):
    if request.method == "POST":
        uname = request.POST['uname']
        passw = request.POST['password']
        cpassw = request.POST['cpassword']
        email = request.POST['email']
        if passw == cpassw:
            if User.objects.filter(username=uname).exists() or User.objects.filter(email=email).exists():
                messages.error(request, 'Username/Email Already Exists')
            else:
                query = User.objects.create(
                    first_name=request.POST['fname'], last_name=request.POST['lname'], username=uname, email=email, password=passw)
                query.set_password(passw)
                query.save()
                messages.success(request, "Succesfully Registered")
                return redirect(login_user)
        else:
            messages.info(request, 'Password Dont MAtch')
            return redirect(register)

    return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['password']
        if username != "" and password != "":
            query = authenticate(request, username=username, password=password)
            if query is None:
                messages.error(request, "Invalid Credentials")
            else:
                login(request, query)
                return redirect(delivery_details)
        else:
            messages.warning(request, "Null Values are not allowed")
    return render(request, 'login.html')


@login_required(login_url="/login")
def delivery_details(request):
    try:
        existing_delivery_address = DeliveryAddress.objects.get(
            username=request.user)

        if existing_delivery_address:
            return redirect(index)
        else:
            if request.method == "POST":
                mob = request.POST['mob']
                alt_mob = request.POST['altermob']
                pincode = request.POST['pincode']
                address = request.POST.get('address')
                state = request.POST.get('state')
                country = request.POST.get('country')
                deliverytype = request.POST.get('dt')

                if mob and alt_mob and pincode and address and state and country and deliverytype:
                    query = DeliveryAddress.objects.create(
                        username=request.user,
                        mobile=mob,
                        altmob=alt_mob,
                        pincode=pincode,
                        address=address,
                        dtype=deliverytype,
                        state=state,
                        country=country
                    )
                    query.save()
                    messages.success(
                        request, "Delivery address added successfully.")
                    return render(request, 'index.html')
                else:
                    messages.info(request, "No fields can have null values.")
            return render(request, 'order.html')
    except DeliveryAddress.DoesNotExist:
        if request.method == "POST":
            mob = request.POST['mob']
            alt_mob = request.POST['altermob']
            pincode = request.POST['pincode']
            address = request.POST.get('address')
            state = request.POST.get('state')
            country = request.POST.get('country')
            deliverytype = request.POST.get('dt')

            if mob and alt_mob and pincode and address and state and country and deliverytype:
                query = DeliveryAddress.objects.create(
                    username=request.user,
                    mobile=mob,
                    altmob=alt_mob,
                    pincode=pincode,
                    address=address,
                    dtype=deliverytype,
                    state=state,
                    country=country
                )
                messages.success(
                    request, "Delivery address added successfully.")
                return render(request, 'index.html')
            else:
                messages.info(request, "No fields can have null values.")
        return render(request, 'order.html')
    except Exception as e:
        messages.warning(request, f"Error occurred: {e}")
        return render(request, 'order.html')


def logout_user(request):
    if request.method == "POST":

        logout(request)
    return redirect('login')


def product_page(request, category):
    query = Products.objects.filter(category=category)
    return render(request, 'product_page.html', {"query": query})


@login_required(login_url='/login')
def add_cart(request, item):
    product = get_object_or_404(Products, pro_name=item)
    if product:
        query2 = Cart.objects.create(
            username=request.user, item_name=product.pro_name, item_price=product.pro_price)
    return redirect(account)


@login_required(login_url='/login')
def account(request):
    query = Cart.objects.filter(username=request.user)
    return render(request, 'accounts.html', {"query": query})


def remove_cart(request, id):
    query = Cart.objects.get(id=id).delete()
    if query:
        messages.info(request, "item removed")
    return redirect(account)


@login_required(login_url='/login')
def billing(request, id):

    if request.method == "POST":
        quantity = request.POST.get('quantity')
        deliveron=request.POST['deliveron']
        query = get_object_or_404(Products, id=id)

        proprice = query.pro_price

        totalamount = int(proprice)*int(quantity)

        query2 = DeliverProducts.objects.create(username=request.user, product=query, quantity=int(
            quantity), paymentmod="COD", total_amount=totalamount,deliveron=deliveron)
        messages.info(
            request, "Succesfully Ordered .You will receive product within 7 days")
        return redirect(ordered_products)
    return render(request, 'billing.html')


@login_required(login_url='/login')
def ordered_products(request):
    query = DeliverProducts.objects.filter(
        username=request.user).filter(Status="pending")

    return render(request, 'orderedproducts.html', {"query": query})


def cancelled_view(request):
    query = DeliverProducts.objects.filter(
        username=request.user).filter(Status="canceled")
    return render(request, 'cancled.html', {"query": query})


def cancel_order(request, id):
    query = DeliverProducts.objects.filter(id=id).update(Status="canceled")
    if query:
        messages.info(request, "item canceled")
        return redirect(cancelled_view)
    
def delete_order(request, id):
    query = DeliverProducts.objects.get(id=id).delete()
    if query:
        messages.info(request, "item deleted")
    return redirect(account)