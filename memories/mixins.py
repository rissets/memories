import datetime
import json
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.http import JsonResponse, request, response
from django.shortcuts import redirect


def form_errors(*args):
    """
    Handles form error that are passed back to AJAX calls
    """
    message = ""
    for f in args:
        if f.errors:
            message = f.errors.as_text()
    return message


def recaptcha_validation(token):
    """recaptcha validation"""
    result = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': token
        }
    )
    return result.json()


class AjaxFormMixin(object):
    """
    Mixin to ajaxify django form - can be over written in view by calling form_valid method
    """

    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            message = form_errors(form)
            return JsonResponse({'result': 'Error', 'message': message})
        return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            form.save()
            return JsonResponse({
                'result': 'Success',
                'message': ''
            })
        return response

