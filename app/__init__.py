from django.shortcuts import render as render_template
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.http import HttpResponse


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except:
        return None

def is_post(request):
    return request.method == 'POST'

def is_htmx(request):
    return 'HX-Request' in request.headers

def render(request, template:str, title='Borno State Scholarship Board', *args, **kwargs):
    kwargs.setdefault('title', title)

    if not template.endswith('.html'):
        template = f"{template}.html"
    
    return render_template(request, template, *args, kwargs)

def render_form(request, form):
    ctx = {}
    ctx.update(csrf(request))
    return HttpResponse(render_crispy_form(form, context=ctx))