from django.shortcuts import redirect
from django.contrib import messages
from app import render, is_post 
from .forms import Registration, RegistrationForm

# Create your views here.
def index(request): 
    registration = Registration.load()
    form = RegistrationForm(instance=registration)
    

    if is_post(request):
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid() and form.save():
            messages.success(request, 'Registration constraints updated success fully!')
            return redirect(request.path)
    
    return render(
        request, 'registration/index',
        title='BSSB Manage Registraion',
        registration = registration,
        form = form,
    )