from django.db import models
from django.core.files import File
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.utils import timezone


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=email,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='ایمیل',
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True, max_length=255, verbose_name="نام کاربری")
    email = models.CharField(unique=True, max_length=66, verbose_name='ایمیل')
    is_active = models.BooleanField(default=True, verbose_name="کاربر فعال و اجاره ورود دارد")
    is_admin = models.BooleanField(default=False, verbose_name="کاربر ادمین اصلی است")
    is_taiid_for_shop = models.BooleanField(default=False,verbose_name="کاربر توسظ مدیر سایت تایید شده و می تواند به پنل فروشکاهی خود وارد شود ")
    is_ban = models.BooleanField(default=False, verbose_name="کاربر مسدود است!")

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="profiles")
    first_name = models.CharField(max_length=50, blank=True, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=False)
    phone = models.CharField(max_length=11, blank=True, null=False)
    adress = models.CharField(max_length=200, blank=True, null=False)
    image = models.ImageField(upload_to='profile_image/')


def save_profile_user(sender, **kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user, sender=MyUser)
