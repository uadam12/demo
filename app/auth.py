from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


def login_required(view):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'You need to login to access this page.')
            return redirect('user:login')

        if not request.user.is_active:
            messages.info(request, 'You need to activate your to access this page.')
            return redirect('user:activation')
        
        return view(request, *args, **kwargs)
    return wrapper

def logout_required(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already authenticated.')
            return redirect(request.user.dashboard)

        return view(request, *args, **kwargs)
    return wrapper

def inactive_required(view):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_active:
            messages.info(request, 'Your account is already activated.')
            return redirect(request.user.dashboard)
        
        return view(request, *args, **kwargs)
    return wrapper

def blocked_required(view):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.access_code > 0:
            return redirect(request.user.dashboard)
        
        return view(request, *args, **kwargs)
    return wrapper


def applicant_only(view):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.access_code == 0:
            messages.error(request, 'Looks like your account is blocked.')
            return redirect('user:block')

        if request.user.access_code != 1:
            messages.info(request, 'This page is for applicant only.')
            return redirect('official:dashboard')
        
        if  request.user.paid_registration_fee:
            messages.info(request, 'You need to pay registration fee')
            return redirect('payment:registration-fee')

        return view(request, *args, **kwargs)
    return wrapper
        
def officials_only(admin_only=False, main_admin_only=False):
    def officials_deco(view):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.access_code < 2:
                messages.error(request, 'This page is for officials only.')
                logout(request)
                return redirect('user:login')
            
            if admin_only and request.user.access_code == 2:
                messages.info(request, 'This page is for admins only.')
                return redirect('official:dashboard')
             
            if main_admin_only and request.user.access_code < 4:
                messages.info(request, 'This page is for main admins only.')
                return redirect('official:dashboard')
            return view(request, *args, **kwargs)
        return wrapper
    return officials_deco