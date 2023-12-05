from django.shortcuts import get_object_or_404, render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

# Create your views here.


def index(request):
    mobiles = Products.objects.filter(
        category="smartphone").filter(pro_rating__gte=4.3)[:8]
    laptop = Products.objects.filter(
        category="laptops").filter(pro_rating__gt=4)[:8]
    blog = Blogs.objects.all().order_by('?')[:4]
    review = Reviews.objects.all().order_by('?')
    banner = Banners.objects.all().order_by('?')
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        if name and email and phone and message != "":
            Contactus.objects.create(
                name=name, email=email, phone=phone, message=message)
            messages.info(request, 'Thankyou for your feedback')
            return redirect(index)
        else:
            messages.info(request, 'Sorry Null values are not allowed')
            return redirect(index)

    return render(request, 'index.html', {"mobiles": mobiles, "laptop": laptop, "blog": blog, "review": review, "banner": banner})


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
    query = Products.objects.filter(category=category).order_by('?')
    return render(request, 'product_page.html', {"query": query})


@login_required(login_url='/login')
def add_cart(request, item):
    product = get_object_or_404(Products, pro_name=item)
    if product:
        query2 = Cart.objects.create(
            username=request.user, item_name=product.pro_name, product_id=product.id, item_price=product.pro_price)
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
        deliveron = request.POST['deliveron']
        query = get_object_or_404(Products, id=id)

        proprice = query.pro_price
        proname = query.pro_name

        totalamount = int(proprice)*int(quantity)

        query2 = DeliverProducts.objects.create(username=request.user, product=query, quantity=int(
            quantity), paymentmod="COD", total_amount=totalamount, deliveron=deliveron)
        Cart.objects.filter(item_name=proname).delete()
        messages.info(
            request, "Succesfully Ordered .You will receive product on selected date")
        return redirect(ordered_products)
    return render(request, 'billing.html')


@login_required(login_url='/login')
def ordered_products(request):
    query = DeliverProducts.objects.filter(
        username=request.user).filter(Q(Status="pending") | Q(Status="dispatched"))

    return render(request, 'orderedproducts.html', {"query": query})


def cancelled_view(request):
    query = DeliverProducts.objects.filter(
        username=request.user).filter(Status="canceled")
    return render(request, 'cancled.html', {"query": query})


def delivered_order(request):
    query = DeliverProducts.objects.filter(
        username=request.user).filter(Status="delivered")
    return render(request, 'delivered.html', {"query": query})


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


@login_required(login_url="/login")
def create_blog(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']

        image = request.FILES['images']

        if title and description and image != "":
            Blogs.objects.create(
                username=request.user, title=title, description=description, image=image)
            messages.info(request, "Blog Created")
            return redirect(my_blogs)
        else:
            messages.info(request, "Sorry null vales are not allowed")
            return redirect(create_blog)
    return render(request, 'createblog.html')


@login_required(login_url="/login")
def my_blogs(request):
    query = Blogs.objects.filter(username_id=request.user)
    return render(request, 'myblogs.html', {"query": query})


@login_required(login_url="/login")
def edit_blogs(request, id):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']

        if 'images' in request.FILES:
            image = request.FILES['images']
            print(image)
        else:
            image = None

        if title and description != "":
            if image:
                query2 = Blogs.objects.get(id=id)
                query2.title = title
                query2.description = description
                query2.image = image
                query2.save()

                messages.info(request, "Blog Updated")
                return redirect(my_blogs)
            else:
                query2 = Blogs.objects.get(id=id)
                query2.title = title
                query2.description = description

                query2.save()

                messages.info(request, "Blog Updated")
                return redirect(my_blogs)

        else:
            messages.info(request, "Sorry null vales are not allowed")
            return redirect(create_blog)
    query = Blogs.objects.filter(username_id=request.user).filter(id=id)
    return render(request, 'editblog.html', {"query": query})


@login_required(login_url="/login")
def delete_blog(request, id):
    Blogs.objects.filter(id=id).delete()
    return redirect(my_blogs)


@login_required(login_url='/login')
def add_review(request):

    if request.method == "POST":

        comment = request.POST['comment']
        if comment != "":
            Reviews.objects.create(username=request.user, review=comment)
            return redirect(index)


def all_blogs(request):
    blog = Blogs.objects.all().order_by('?')
    return render(request, 'allblogs.html', {'blog': blog})


@login_required(login_url='/login')
def update_address(request):

    if request.method == "POST":

        mob = request.POST['mob']
        alt_mob = request.POST['altermob']
        pincode = request.POST['pincode']
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        dt = request.POST.get('dt')

        DeliveryAddress.objects.filter(username_id=request.user).update(mobile=mob,
                                                                        altmob=alt_mob,
                                                                        pincode=pincode,
                                                                        address=address,
                                                                        dtype=dt,
                                                                        state=state,
                                                                        country=country)
        messages.info(request, 'Details Updated Successfully')

    query = DeliveryAddress.objects.filter(username_id=request.user)

    return render(request, 'updateadd.html', {"query": query})


@login_required(login_url='/login')
def myaddress(request):
    query = DeliveryAddress.objects.filter(username_id=request.user)
    return render(request, 'myaddress.html', {"query": query})


def search_items(request):
    try:
        if request.method == "GET":
            name = request.GET.get('name')
            query = Products.objects.filter(Q(pro_name__icontains=name) | Q(pro_desc__icontains=name) | Q(
                pro_brand__icontains=name) | Q(category__icontains=name) | Q(pro_price__icontains=name))
            return render(request, 'search.html', {"query": query})
    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect(index)


def checkoutall(request):
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        deliveron = request.POST['deliveron']
        query = Cart.objects.filter(username_id=request.user)
        for val in query:
            query2 = get_object_or_404(Products, pro_name=val.item_name)

            totalamount = int(quantity) * int(val.item_price)

            DeliverProducts.objects.create(
                username=request.user,
                product=query2,
                quantity=int(quantity),
                paymentmod="COD",
                total_amount=totalamount,
                deliveron=deliveron
            )

            val.delete()
        messages.info(
                request, "Succesfully Ordered .You will receive products on selected date")
        return redirect(ordered_products)

    return render(request, 'cartbilling.html')
