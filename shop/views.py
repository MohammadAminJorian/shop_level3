from django.shortcuts import render
from django.shortcuts import render, redirect , get_object_or_404
from .models import *
from shop.models import *
from users.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied

import random
# Create your views here.
def is_taiid_for_shop(func):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_taiid_for_shop:
            return redirect("shop:nottaiid")
            raise PermissionDenied
        return func(request,*args,**kwargs)
    return wrapper

    

def is_ban(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.is_ban:
                return redirect("shop:isban")
                raise PermissionDenied
        return func(request,*args,**kwargs)
    return wrapper


@is_ban
def home(request):
    categorys = Category.objects.filter(position='1')
    context = {'categorys': categorys}
    return render(request, "home/home.html" , context)


def isban(request):
    return render(request, "errors/userisban.html")



def nottaiid(request):
    return render(request, "errors/nottaiid.html")


def about(request):
    return render(request, "contact/about.html")


def taiid(request):
    return render(request, "home/taiid.html")



@login_required(login_url='/login/')
def Contact_To_admin(request):
    if request.method == "POST":
        name = request.POST['name']
        message = request.POST['message']
        mozo = request.POST['mozo']


        Contact_to_admin.objects.create(name=name, message=message , mozo=mozo)
        messages.success(request, 'پیام شما با موفقیت ارسال شد ')
        return redirect('shop:home')

    user = MyUser.objects.filter(id=request.user.id)
    profile = Profile.objects.filter(user_id=request.user.id)

    context = {
        'user': user,
        'profile': profile,

    }
    return render(request, 'contact/contacttoadmin/contacttoadmin.html' ,context)




@login_required(login_url='/login/')
def requestu(request):
    if request.method == 'POST':
        repuest_form = RequestUserForm(request.POST, request.FILES, instance=request.user.requestuser)
        if repuest_form.is_valid():
            repuest_form.save()
            messages.success(request, 'درخواست شما با موفقیت ارسال شد تا 24 ساعت دیگر منتطر تماس پشتیبانی بمانید')
            return redirect('shop:home')
    else:
        repuest_form = RequestUserForm(instance=request.user.requestuser)
    context = {'repuest_form': repuest_form}
    return render(request, 'home/taiid.html', context)





@login_required(login_url='/login/')
@is_taiid_for_shop
def shoppanel(request):
    return render(request, "shoppanel/shoppanel.html")



@login_required(login_url='/login/')
def ProfileShopEdit(request):
    if request.method == 'POST':
        profile_shop_form = ProfileShopEditForm(request.POST, request.FILES, instance=request.user.shop)
        print(profile_shop_form)
        if profile_shop_form.is_valid():
            profile_shop_form.save()
            messages.success(request, 'اطلاعات فروشگاه شما با موفقیت تغییر کرد')
            return redirect('shop:home')
    else:
        profile_shop_form = ProfileShopEditForm(instance=request.user.shop)
    context = {'profile_shop_form': profile_shop_form}
    return render(request, 'shoppanel/shopprofile/editprofile.html', context)



@login_required(login_url='/login/')
def ViewProfileShop(request):
    profile_shop = Shop_panel_profile.objects.filter(user_id=request.user.id)
    context = {
        'profile_shop': profile_shop
    }
    return render(request, 'shoppanel/shopprofile/showprofile.html', context)



@is_taiid_for_shop
def create_product(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST , request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            messages.success(request, 'محصول شما با موفقیت ثبت شد')
            post.save()
            return redirect('shop:dashbord')
    else:
        form = CreateProductForm()
        categoryy = Category.objects.all()
    return render(request, 'shoppanel/addproduct/addproduct.html', {'form': form ,'categoryy':categoryy })





def ViewProduct(request ):
    products = Product.objects.filter(status='p').order_by('-publish')
    productss = Product.objects.all()
    context = {
        'products': products,
        'productss': productss
               }
    return render(request, 'shop/productview.html', context)



@login_required(login_url='/login/')
def dashbord(request):
    return render(request, "shoppanel/shopprofile/dashbord.html")



def categoryview(request):
    categorys = Category.objects.all()
    context = {'categorys': categorys}
    return render(request, 'shop/categoryview.html', context)



@login_required(login_url='/login/')
def detail_product(request, slug):
    global num
    detail = get_object_or_404(Product, slug=slug, status='p')
    productm = Product.objects.all()
    product = productm.filter(slug=slug)
    num = request.POST.get('num')


    context = {
        'detail': detail,
        'product' : product
    }
    return render(request, 'shop/detailproduct.html', context)





@login_required(login_url='/login/')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)


    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    global num

    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,
                                                        user=request.user)
    cart_item.quantity += int(num)
    cart_item.save()
    num = None
    return redirect('shop:view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('shop:view_cart')




@login_required(login_url='/login/')
def myCourse(request,id):
    cart = Cart.objects.filter(user_id=id)
    for carts in cart:
        video = Video.objects.filter(id = carts.video_id)
        context = {'video':video}
        return render(request, 'administrator/course/myCourse.html',context)

    return render(request, 'administrator/course/myCourse.html')