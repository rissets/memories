
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserCreationForm)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Profile


class AccountsForm(UserCreationForm):
    """
    form that uses built-in UsercreationForm to handle user creation.
    """

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('*Your first name..'),
                'class': 'input',
            }
        )
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('*Your last name..'),
                'class': 'input',
            }
        )
    )
    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('*Email'),
                'class': 'input',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('*Password'),
                'class': 'input password-input'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('*Confirm Password'),
                'class': 'input password-input',
            }
        )
    )

    # reCapctha token
    token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError(_("Username already exists"))
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(_('Passwords do not match.'))
        return cd['password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': _('*Email..'),
                }
            )
        )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input password-input',
                'placeholder': _('*Password..'),
                # 'data-eye': 'True'
                }
            )
        )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'agreement-checkbox',
                'id': 'remember-1'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class PassResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New Password',
                'id': 'form-newpass',
                'data-eye': 'True'
            }
        )
    )
    new_password2 = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New Password',
                'id': 'form-newpass2',
                'data-eye': 'True'
            }
        )
    )


class PassResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'id': 'form-email'
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        test = User.objects.filter(email=email)
        if not test:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address'
            )
        return email



class PassChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label='Old Password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-oldpass'}))
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': _('First Name'), 'id': 'form-firstname'}))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': _('Last Name'), 'id': 'form-lastname'}))

    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': _('*Email..')}))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = False


class AccountProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update(
            {
                'class': ' input-file',
                'id': 'profile-userpic',
            }
        )


