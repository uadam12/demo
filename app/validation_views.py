from django.http import HttpResponse
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from users.forms import RegisterForm

def nin(request):
    form = RegisterForm(request.POST)
    form.is_valid()
    return HttpResponse(as_crispy_field(form['nin']))

def bvn(request):
    form = RegisterForm(request.POST)
    form.is_valid()
    return HttpResponse(as_crispy_field(form['bvn']))

def email(request):
    form = RegisterForm(request.POST)
    form.is_valid()
    return HttpResponse(as_crispy_field(form['email']))

def phone_number(request):
    form = RegisterForm(request.POST)
    form.is_valid()
    return HttpResponse(as_crispy_field(form['phone_number']))