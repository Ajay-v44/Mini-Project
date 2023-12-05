"""ecomerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="home"),
    path('register/', register, name='register'),
    path('login/', login_user, name="login"),
    path('orderdetails/', delivery_details, name="delivery"),
    path('logout/', logout_user, name="logout"),
    path('productpage/<str:category>', product_page, name="product"),
    path('add_cart/<str:item>', add_cart, name="add_cart"),
    path('account/', account, name="account"),
    path('remove/<int:id>', remove_cart, name="remove"),
    path('billing/<int:id>/', billing, name='billing'),
    path('orderedproducts/', ordered_products, name='orderedproducts'),
    path(' cancelorder/<int:id>', cancel_order, name=' cancelorder'),
    path('cancelledview/', cancelled_view, name='cancelledview'),
    path('deleteorder/<int:id>', delete_order, name='deleteorder'),
    path('delivered/', delivered_order, name="delivered"),
    path('createblogs/', create_blog, name='createblogs'),
    path('myblogs/', my_blogs, name='myblogs'),
    path('editblogs/<int:id>', edit_blogs, name='editblogs'),
    path('deleteblog/<int:id>', delete_blog, name='deleteblog'),
    path('addreview/', add_review, name='addreview'),
    path('allblogs/', all_blogs, name='allblogs'),
    path('updatedelivery/',update_address,name='updatedelivery'),
    path('myaddress/',myaddress,name='myaddress'),
    path('search/',search_items,name='search'),
    path('checkoutall/',checkoutall,name='checkoutall')
    
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
