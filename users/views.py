from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
import random


# Create your views here.




def Login(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, 'ورود. خوش آمدید')
            login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
            context = {
                "username": username,
                "errormessage": "User not found"
            }
            return render(request, "login/login.html", context)
    else:
        return render(request, 'login/login.html', {})


def Register(request):
    if request.user.is_authenticated:
        return redirect('shop:home')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        username = form['username'].value()
        email = form['email'].value()
        if MyUser.objects.filter(username=username).exists():
            messages.error(request, 'نام کاربری شما تکراری است.')
            return redirect('users:register')
        if MyUser.objects.filter(email=email).exists():
            messages.error(request, 'ایمیل شما تکراری است')
            return redirect('users:register')
        if form.is_valid():
            data = form.cleaned_data
            user = MyUser.objects.create_user(email=data['email'], username=data['username'], password=data['password'])
            user.save()
            messages.success(request, 'حساب کاربری شما با موفقیت ساخته شد')
            return redirect('users:login')
        else:
            messages.error(request, 'خطای غیر منتطره رخ داد . در صورت دیدن این پیغام با مدیر سایت در ارتباط باشید')
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'register/register.html', context)


def Logout(request):
    logout(request)
    return redirect('shop:home')


@login_required(login_url='/login/')
def ViewProfile(request):
    profile = Profile.objects.filter(user_id=request.user.id)
    myuser = MyUser.objects.filter(id=request.user.id)

    context = {
        'profile': profile,
        'myuser': myuser
    }
    return render(request, 'profile/viewprofile/viewprofile.html', context)


@login_required(login_url='/login/')
def delete_user(request, email):
    if request.method == 'POST':
        try:
            user = MyUser.objects.get(email = email)
            user.delete()
        except Exception as e:
            print(e)
    else:
        messages.error(request, 'اکانت شما حذف شد')
    return render(request, 'shop/profile/delete.html')


@login_required(login_url='/login/')
def ProfileEdit(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profiles)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'پروفایل شما با موفقیت تغییر کرد')
            return redirect('shop:home')
    else:
        profile_form = ProfileEditForm(instance=request.user.profiles)
    context = {'profile_form': profile_form}
    return render(request, 'profile/editprofile/editprofile.html', context)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'passwordReset/password_reset.html'
    email_template_name = 'passwordReset/password_reset_email.html'
    subject_template_name = 'passwordReset/password_reset_subjects'

    success_url = reverse_lazy('users:login')




