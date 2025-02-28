from django.db import models
from django.utils import timezone
from django.db import models
from users.models import *
from django.db.models.signals import post_save


class Contact_to_admin(models.Model):
    name = models.CharField(max_length=40, verbose_name="نام ارسال کننده پیغام")
    mozo = models.CharField(max_length=40, verbose_name="موضوع")
    message = models.TextField(verbose_name='پیغام')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')

    def __str__(self):
        return self.mozo


class Contact_to_user(models.Model):
    STATUS_CHOICES = (
        ('p', 'ارسال شود'),
        ('d', 'ذخیره شود بعدا ارسال می کنم')
    )
    view = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="...ارسال شود به ", related_name='view')
    name = models.CharField(max_length=40, verbose_name="نام و نام خانوادگی ارسال کننده پیام")
    mozo = models.CharField(max_length=80, verbose_name="موضوع")
    image = models.ImageField(upload_to='image/', verbose_name='عکس')
    message = models.TextField(verbose_name='پیغام')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار این پیام')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="نوع وضغیت را انتخاب کنید")
    seen = models.BooleanField(default=False, verbose_name="کاربر پیغام شما را سین کرده است ")

    def __str__(self):
        return self.view.username


class Shop_panel_profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="shop")
    name_of_shop = models.CharField(max_length=50, blank=True, null=False)
    desc = models.CharField(max_length=50, blank=True, null=False)
    avatar = models.ImageField(upload_to='avatar/')
    adress = models.CharField(max_length=200, blank=True, null=False)
    phone_of_owner = models.CharField(max_length=11, blank=True, null=False)
    phone_of_shop = models.CharField(max_length=11, blank=True, null=False)
    code_melli_of_owner = models.CharField(max_length=10, blank=True, null=False)


    def __str__(self):
        return self.name_of_shop


def shop_panel_user(sender, **kwargs):
    if kwargs['created']:
        shop_panel_user = Shop_panel_profile(user=kwargs['instance'])
        shop_panel_user.save()


post_save.connect(shop_panel_user, sender=MyUser)


class Category(models.Model):
    title = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    desc = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_image/')
    position = models.IntegerField()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS_CHOICES = (
        ('p', 'publish'),
        ('d', 'draft')
    )
    owner = models.ForeignKey(MyUser ,on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)
    desc = models.TextField()
    tedad = models.IntegerField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE ,related_name="post")
    image = models.ImageField(upload_to='productimage/')
    num = models.CharField(max_length=20 ,blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title




class RequestU(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="requestuser")
    text = models.CharField(max_length=50, blank=True, null=False)


def save_request_user(sender, **kwargs):
    if kwargs['created']:
        save_request_user = RequestU(user=kwargs['instance'])
        save_request_user.save()

post_save.connect(save_request_user, sender=MyUser)



class CartItem(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'