from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from app import render, is_post
from app.views import update_view
from app.token import verify_token
from app.auth import login_required, logout_required, blocked_required
from board.models import LGA
from applicant.models import PersonalInformation
from payment.remita import remita
from .forms import RegisterForm, LoginForm, EmailForm, UserForm, ProfilePictureForm, ResetPasswordForm
from .emails import send_activation_email, send_recovery_email

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
        success_url='applicant:profile',
        form_class=UserForm,
        header='Update name',
        template='users/update-name'
    )

@logout_required
def register(request):
    form = RegisterForm
    
    if is_post(request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            nin = data.get('nin', '')
            bvn = data.get('bvn', '')
            
            nin_data = remita.get_nin_data(nin)
            bvn_data = remita.get_bvn_data(bvn)
            nin_state_code = nin_data.get('stateOfOriginCode', '')
            bvn_state_code = bvn_data.get('stateOfOriginCode', '')
            lga_code = nin_data.get('lgaofOriginCode', '')
            
            if nin_state_code != 'BO' or bvn_state_code != 'BO':
                error = 'You are not applicable for this program'
                form.add_error('nin', error)
                form.add_error('bvn', error)

            else:
                lga = LGA.objects.filter(code=lga_code).first()
                nin_date_of_birth = nin_data.get('dateOfBirth', '')
                bvn_date_of_birth = bvn_data.get('dateOfBirth', '')
                nin_firstname = nin_data.get('firstName', '')
                nin_lastname = nin_data.get('lastName', '')
                nin_gender = nin_data.get('gender')
                
                if nin_date_of_birth == bvn_date_of_birth:
                    form.add_error(None, 'Data mismatch')
                else:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.first_name = nin_firstname
                    user.last_name = nin_lastname
                    sent = send_activation_email(request, user)

                    if sent:
                        personal_info = PersonalInformation(
                            phone_number = data.get('phone_number'),
                            gender = nin_gender,
                            date_of_birth = nin_date_of_birth,
                            nin = nin, bvn = bvn, user = user,
                            local_government_area = lga
                        )                        
                        
                        user.save()
                        personal_info.save()
                        login_user(request, user)
                        messages.success(request, 'Account created successfully!')
                        return redirect('user:inactive')


    return render(
        request, 'users/register',
        title = 'BSSB Registration',
        form = form
    )

def activate(request, token):
    User = get_user_model()
    email = verify_token(token)
    print(email)
    user = User.objects.filter(email=email)
    
    if user.exists():
        user = user.first()
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can complete your profile information.')
        return redirect('applicant:profile')
    
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
            user = get_user_model().objects.filter(email=email)

            if user.exists():
                user = user.first()
                
                sent = send_recovery_email(request, user)
                if sent:
                    messages.success(request, 'Account recovery instruction(s) sent successfully.')
            
    return render(request, 'users/forgot-password', title='BSSB Forgot password', form=form)

@logout_required
def reset_password(request, token):
    email = verify_token(token)
    
    if not email:
        return redirect('user:login')

    user = get_user_model().objects.filter(email=email)
    if not user.exists():
        messages.error(request, 'No account is associated with this email address')
        return redirect('user:login')

    form = ResetPasswordForm()
    
    if is_post(request):
        form = ResetPasswordForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            user = user.first()
            user.set_password(password)
            user.save()
            messages.success(request, 'Password updated successfully. Try your new password.')
            return redirect('user:login')


    return render(request, 'users/reset-password', 'BSSB | Reset Password', form=form)

@blocked_required    
def block(request):
    return render(request, 'users/block', 'BSSB | Block account')