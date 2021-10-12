from blog.models import Category, Post
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormView
from taggit.models import Tag

from memories.mixins import AjaxFormMixin, form_errors, recaptcha_validation

from .forms import (AccountProfileForm, AccountsForm, UserLoginForm,
                    UserProfileForm)
from .token import account_activation_token

result = _("Error")
message = _("There was an error, please try again!")


class SignUpView(AjaxFormMixin, FormView):
    """
    Generic FormView with our mixin for sign-up with reCAPTURE security.
    """

    template_name = "accounts/sign_up.html"
    form_class = AccountsForm
    success_url = "{{accounts:sign-in}}"

    # reCAPTURE key required in context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recaptcha_site_key"] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            token = form.cleaned_data.get('token')
            captcha = recaptcha_validation(token)
            if captcha["success"]:
                user = form.save(commit=False)
                user.email = user.username
                user.save()
                profile = user.profile
                profile.captcha_score = float(captcha["score"])
                profile.is_active = False
                profile.save()
                current_site = get_current_site(self.request)
                subject = _('Activate your Account')
                message_activate = render_to_string('accounts/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject=subject, message=message_activate)

                login(self.request, user,
                      backend='django.contrib.auth.backends.ModelBackend')

                # change result & message on success
                result = _("Success")
                message = _("Thank you for signing up and activation sent")

            data = {'result': result, 'message': message}
            return JsonResponse(data)

        return response


class SignInView(AjaxFormMixin, FormView):
    """
    Generic FormView with our mixin for user sign-in
    """
    template_name = 'accounts/sign_in.html'
    form_class = UserLoginForm
    success_url = 'accounts/profile'

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # get remember me data from cleaned_data of form
            remember_me = form.cleaned_data.get('remember_me')
            if not remember_me:
                self.request.session.set_expiry(0)  # if remember me is
                self.request.session.modified = True

            # attempt to authenticate user
            user = authenticate(
                self.request, username=username, password=password)
            if user is not None:
                login(self.request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                result = _("Success")
                message = _("You are now logged in!")
            else:
                message = form_errors(form)

            data = {'result': result, 'message': message}
            return JsonResponse(data)

        return response


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        profile = user.profile
        profile.email_confirmed = True
        profile.has_profile = True
        profile.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, _("Success!   Your account is acctive now."))
        return redirect('accounts:sign-in')
    else:
        messages.errors(request, _("Errors! Your account is active"))
        return render(request, 'accounts/activation_invalid.html')


@login_required
def sign_out(request):
    """
    Basic view for user sign out
    """
    logout(request)
    data = {
        'result': 'Success',
        'message': _('You are now logged out')
    }
    return JsonResponse(data)


@login_required
def profile_view(request):
    """
    Function view to allow users to update theri profile
    """

    result = "Errors"
    message = ""

    user_form = UserProfileForm(instance=request.user)
    profile_form = AccountProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserProfileForm(instance=request.user, data=request.POST)
        profile_form = AccountProfileForm(
            data=request.POST, files=request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():
            # obj = profile_form.save()
            # if User.objects.filter(username=obj.username).exclude(username=request.user.username).exists():
            #     result = "Errors"
            #     message = _("Please use another username, that is already taken")
            # else:
            # obj.has_profile = True
            # obj.save()

            profile_form.save()
            user_form.save()
            result = "Success"
            message = _("Your profile has been updated")
        else:
            result = "Error"
            message = form_errors(profile_form)

        data = {'result': result, 'message': message}
        return JsonResponse(data)

    else:

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

    return render(request, 'accounts/profile.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(instance=request.user, data=request.POST)
        profile_form = AccountProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid() and user_form.is_valid():
            # new_user_form = user_form.save(commit=False)
            # print(User.objects.filter(email=new_user_form.email))
            # if User.objects.filter(email=new_user_form.email).exclude(email=request.user.email).exists():
            #     messages.error(request, _("Please use another Email, that is already taken"))
            # else:
            messages.success(request, _("Success! Profile updated."))
            user_form.save()
            profile_form.save()

    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = AccountProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def delete_user(request):

    if request.is_ajax():
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        result = "Success"
        message = _("Your account has been deleted")

        data = {'result': result, 'message': message}
        return JsonResponse(data)
    else:
        return render(request, 'accounts/delete.html')


class FavouriteList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'accounts/save_posts.html'
    context_object_name = 'favourite_posts'
    paginate_by = 10

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            favourites=self.request.user).filter(status=True).order_by('-pub_date')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        popular = self.model.objects.filter(status=True, pub_date__range=[timezone.now(
        ) - timezone.timedelta(7), timezone.now()]).annotate(Sum('views')).order_by('-views')[:3]
        context = super().get_context_data(**kwargs)
        context['popular_list'] = popular
        context['allcategories'] = Category.objects.all().annotate(
            posts_count=Count('post'))
        context['tags'] = Tag.objects.all()
        context['all_posts'] = self.model.objects.order_by('pub_date')
        return context


@login_required
def favourite_list(request):

    posts = Post.objects.filter(favourites=request.user).filter(
        status=True).order_by('-pub_date')[:5]
    return render(request, 'accounts/save_posts.html', {'favourite_posts': posts})


@ login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            post.save()
            result_like = post.like_count
            result = "Error"
            message = _("Successfully removed likes")
        else:
            post.likes.add(request.user)
            post.like_count += 1
            post.save()
            result_like = post.like_count
            result = "Success"
            message = _("Thank you for liking the post")

        data = {'result_like': result_like,
                'result': result, 'message': message}
        return JsonResponse(data)


@login_required
def favourite_add(request):
    if request.method == "GET":
        id = request.GET['postfavid']
        post = get_object_or_404(Post, id=id)
        if post.favourites.filter(id=request.user.id).exists():
            post.favourites.remove(request.user)
            result = "Success"
            message = _(
                "Unfortunately the article was successfully removed from favorites.")
        else:
            post.favourites.add(request.user)
            result = "Success"
            message = _("Successfully added to favorites.")

        data = {'result': result, 'message': message}
        return JsonResponse(data)
    return HttpResponse("done")
