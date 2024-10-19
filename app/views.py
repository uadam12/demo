from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from . import render, is_post


def create_view(request, form_class, success_url, form_kwargs={}, header='Recods',  template='create', *args, **kwargs):
    if is_post(request):
        form = form_class(data=request.POST, **form_kwargs)
        
        if form.is_valid() and form.save():
            messages.success(request, f"{header} created successfully!")
            return redirect(success_url)
    else: form = form_class(**form_kwargs)
    
    return render(
        request, template, form=form, 
        back_url=reverse_lazy(success_url),
        title=f"BSSB {header}",
        header=header,
        *args, **kwargs
    )

def update_view(request, instance, form_class, success_url, form_kwargs={}, header='Recods',  template='update', *args, **kwargs):
    if is_post(request):
        form = form_class(instance=instance, data=request.POST, **form_kwargs)
        
        if form.is_valid() and form.save():
            messages.success(request, f"{header} updated successfully!")
            return redirect(success_url)
    else: form = form_class(instance=instance, **form_kwargs)
    
    return render(
        request, template, form=form, 
        model=instance, 
        back_url=reverse_lazy(success_url),
        title=f"BSSB {header}",
        *args, **kwargs
    )
    
def delete_view(request, model, success_url, header='Recods'):
    if is_post(request):
        model.delete()
        messages.success(request, f"{header} deleted successfully!")
        return redirect(success_url)
    
    return render(
        request, 'delete', model=model,
        title=f"BSSB {header}",
        back_url=reverse_lazy(success_url)
    )