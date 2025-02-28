from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/' , Login , name="login"),
    path('register/' , Register , name="register"),
    path('edit_profile/' , ProfileEdit , name="profileUpdate"),
    path('profileView/' , ViewProfile , name="profile_view"),
    path('logout/' , Logout , name="logout"),
    path('delete_user/<str:email>/' , delete_user , name="delete_user"),

    # Forget password
    path('password-reset/', ResetPasswordView.as_view(success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),

    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name="passwordReset/password_reset_done.html"),
         name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete'),
                                                     template_name='passwordReset/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='passwordReset/password_reset_complete.html'),
         name='password_reset_complete'),
]

