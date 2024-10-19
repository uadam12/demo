from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from app import render, is_post
from app.views import update_view
from app.auth import login_required, logout_required
from .token import account_activation_token
from .forms import RegisterForm, LoginForm, EmailForm, UserForm, ProfilePictureForm
from .emails import activate_email

# Create your views here.
@login_required
def change_picture(request):
    return update_view(
        request,
        instance=request.user,
        form_class=ProfilePictureForm,
        success_url='applicant:profile',
        template='users/change-picture'
    )

@login_required
def update_name(request):
    return update_view(
        request,
        instance=request.user,
        form_class=UserForm,
        header='Update name'
    )

@logout_required
def register(request):
    form = RegisterForm
    
    if is_post(request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            activate_email(request, user, form.cleaned_data.get('email'))
            user.is_active = False
            user.save()
            
            #activate_email(request, user, form.cleaned_data.get('email'))

            messages.success(request, 'Account created successfully!')
            messages.info(request, 'We have emailed to the instruction(s) to activate your account!')

            return redirect('user:inactive')
    
    return render(
        request, 'users/register',
        title = 'BSSB Registration',
        form = form
    )

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('user:login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('user:inactive')


@login_required
def inactive(request):
    return render(request, 'users/inactive')

# Create your views here.
@logout_required
def login(request):
    form = LoginForm()
    
    if is_post(request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.data.get('email')
            password = form.data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is None:
                messages.error(request, "Invalid password and/or email address." )
            else:
                login_user(request, user)
                messages.success(request, 'You have login successfully!!!')
                return redirect(user.dashboard)
        else: messages.error(request, str(form.error_messages))
            
    return render(
        request, 'users/login', 
        title = 'BSSB Login',
        form=form
    )

@login_required
def logout(request):
    if is_post(request):
        messages.success(request, 'You have logout successfully!')
        logout_user(request)
    
    return redirect('user:login')

@logout_required
def forgot_password(request):
    form = EmailForm()
    
    if is_post(request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            messages.success(request, email)
            
    return render(request, 'users/forgot-password', title='BSSB Forgot password', form=form)

def block(request):
    return render(request, 'users/block', 'BSSB | Block account')