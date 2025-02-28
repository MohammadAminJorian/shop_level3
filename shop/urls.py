from django.urls import path
from .views import *


app_name = 'shop'

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('nottaiid/', nottaiid, name="nottaiid"),
    path('isban/', isban, name="isban"),
    path('shoppanel/', shoppanel, name="shoppanel"),
    path('create_product/', create_product, name="create_product"),
    path('ProfileShopEdit/', ProfileShopEdit, name="ProfileShopEdit"),
    path('ViewProfileShop/', ViewProfileShop, name="ViewProfileShop"),
    path('ViewProduct/', ViewProduct, name="ViewProduct"),
    path('RequestForShopPanel/', requestu, name="requestu"),
    path('taiid/', taiid, name="taiid"),
    path('add_to_cart/<int:id>', add_to_cart, name="add_to_cart"),
    path('cart/', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('dashbord/', dashbord, name="dashbord"),
    path('categoryview/', categoryview, name="categoryview"),
    path('contact_to_admin/', Contact_To_admin, name="contact_to_admin"),
    path('detail_product/<slug:slug>/', detail_product, name="detail_product"),

]