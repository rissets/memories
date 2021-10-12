from blog.models import Category, Post
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.core import paginator
# from django.views.generic import ListView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# from portfolio.forms import MessageForm
# from portfolio.models import Portfolio
# from portfolio.views import (email_send, get_about_me, get_categories,
#                              get_clients, get_experiences, get_portfolios,
#                              get_services, get_skills, get_testimonial)

from .mixins import form_errors, recaptcha_validation

result = _("Error")
message = _("There was an error, please try again!")


# def home(request):
#     template_name = 'portfolio/home.html'
#     context = {}
#     paginator = Paginator(get_portfolios().order_by("-pub_date"), 3)

#     if request.method == "POST":
#         forms = MessageForm(request.POST)
#         if forms.is_valid():
#             if request.is_ajax():
#                 token = forms.cleaned_data.get('token')
#                 captcha = recaptcha_validation(token)
#                 if captcha["success"]:
#                     new_message = forms.save(commit=False)
#                     new_message.captcha_score = float(captcha["score"])
#                     data = {
#                         'name': request.POST['name'],
#                         'subject': request.POST['subject'],
#                         'email': request.POST['email'],
#                         'message': request.POST['message']
#                     }
#                     if email_send(data):
#                         new_message.save()
#                         result = "Success"
#                         message = _("Thank you for sending us a message")

#                     data = {'result': result, 'message': message}
#                     return JsonResponse(data)
#         else:
#             messages.error(request, _("OOPS! Bot suspected"))
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#     if request.method == 'GET':
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         forms = MessageForm()
#         context = {
#             'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY,
#             'about_me': get_about_me(),
#             'skills': get_skills(),
#             'experiences': get_experiences(),
#             'services': get_services(),
#             'categories': get_categories(),
#             'clients': get_clients(),
#             'testimonials': get_testimonial(),
#             'recent_posts': recent_posts(),
#             'forms': forms,
#             'page_obj': page_obj
#         }
#     return render(request, template_name, context)


def recent_posts():
    recent_posts = Post.objects.filter(status=True).order_by('-pub_date')[:3]
    return recent_posts


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Post.objects.filter(status=True).order_by('-pub_date')

    def lastmod(self, obj):
        return obj.pub_date

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Category.objects.all().order_by('name')

    def location(self, obj):
        return obj.get_absolute_url()


# class PortfolioSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.8
#     protocol = 'http'

#     def items(self):
#         return Portfolio.objects.all().order_by("-pub_date")

#     def lastmod(self, obj):
#         return obj.pub_date

#     def location(self, obj):
#         return obj.get_absolute_url()


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = "http"

    def items(self):
        return ["blog:home", "accounts:sign-in", "accounts:sign-up"]

    def location(self, item):
        return reverse(item)


def error_403(request, exception):
    data = {
        'title': _("Forbidden (403)"),
        'description': _("Access denied, something doesn't match what you're doing."),
        'posts': recent_posts()
    }
    return render(request, 'error_page.html', data)


def error_404(request, exception):
    data = {
        'title': _("Page not found"),
        'description': _("Sorry but we couldn't find the page that you are looking for."),
        'posts': recent_posts()
    }
    return render(request, 'error_page.html', data)


def error_500(request):
    data = {
        'title': _("Ooops!!! 500"),
        'description': _("Looks like something went wrong!\nWe track these errors automatically, but if the problem persists feel free to contact us."),
        'posts': recent_posts()
    }
    return render(request, 'error_page.html', data)
