from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .token import account_activation_token

def activate_email(request, user, email):
    mail_subject = 'Activate your user account.'
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    
    message = render_to_string('email/activate-account.html', {
        'user': user,
        'domain': domain,
        'uid': uidb64,
        'token': token,
        'protocol': 'https'
        #'protocol': 'https' if request.is_secure() else 'http'
    })
    email_msg = EmailMessage(mail_subject, message, to=[email])
    url = domain+reverse('user:activate', kwargs={
        'uidb64': uidb64, 
        'token': token
    })
    
    messages.error(request, url)

    if email_msg.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {email}, check if you typed it correctly.')
