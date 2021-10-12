
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import PassChangeForm, PassResetConfirmForm, PassResetForm

app_name = 'accounts'

urlpatterns = [
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html',
        form_class=PassChangeForm
        ),
        name="passchange"
    ),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html",
    ), name="password_change_done"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name="password_reset_done"),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name = 'accounts/password_reset_form.html',
        form_class = PassResetForm,
        ),
        name='password_reset'
    ),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        form_class=PassResetConfirmForm
        ),
        name='password_reset_confirm'
    ),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html',
    ), name='password_reset_complete'),

    path('sign-up', views.SignUpView.as_view(), name="sign-up"),
    path('sign-in', views.SignInView.as_view(), name="sign-in"),
    path('sign-out', views.sign_out, name="sign-out"),
    path('profile/delete/', views.delete_user, name='deleteuser'),
    path('profile/', views.profile_view, name='profile'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('fav', views.favourite_add, name='favourite_add'),
    path('save_post/', views.FavouriteList.as_view(), name='save_post'),
    path('like/', views.like, name='like'),
    path('delete/', views.delete_user, name="delete_user"),
]
