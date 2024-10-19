from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from app import render, is_post
from app.auth import login_required, applicant_only
from registration.models import Registration
from scholarship.models import Scholarship
from .models import Payment, ApplicationFEE
from .payment import payment

# Create your views here.
@login_required
def registration_fee(request):
    amount = float(Registration.load().fee)

    if is_post(request):
        verification_url = reverse('payment:verify-reg-fee-payment')
        verification_url = request.build_absolute_uri(verification_url)
        url = payment.url(amount, request.user, verification_url)
        return redirect(url)

    return render(
        request, 'payment/registration-fee',
        title='Pay Registration Fee',
        amount = amount
    )


@applicant_only
def verify_reg_fee_payment(request):
    rrr = request.GET.get('reference', None)
    
    if rrr is not None:
        amount = float(Registration.load().fee)
        payment_verified = payment.verify(ref=rrr, amount=amount)

        if payment_verified:
            Payment.objects.get_or_create(
                amount=amount,
                code = 1,
                rrr=rrr,
                payer=request.user
            )
            request.user.paid_registration_fee = True
            request.user.save()

            messages.success(request, 'Registration FEE paid successfully!!!')
            messages.info(request, 'Please complete your profile information.')
            return redirect('user:profile')

    return render(request, 'payment/verify-payment', title='BSSB Verify Payment')

@applicant_only
def application_fee(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    amount = float(scholarship.application_fee)

    if is_post(request):
        verification_url = reverse('payment:verify-app-fee-payment', kwargs={'id':id})
        verification_url = request.build_absolute_uri(verification_url)
        url = payment.url(amount, request.user, verification_url)
        return redirect(url)

    return render(
        request, 'payment/application-fee',
        title='Pay Registration Fee',
        scholarship = scholarship,
    )
    
@applicant_only
def verify_application_fee(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    rrr = request.GET.get('reference', None)
    
    if rrr is not None:
        amount = float(scholarship.application_fee)
        payment_verified = payment.verify(ref=rrr, amount=amount)

        if payment_verified:
            payment_obj, _ = Payment.objects.get_or_create(
                amount=amount,
                code = 2,
                rrr=rrr,
                payer=request.user
            )
            ApplicationFEE.objects.get_or_create(
                payment = payment_obj,
                applicant = request.user,
                scholarship = scholarship,
            )
            messages.success(request, 'Application FEE paid successfully!!!')
            messages.info(request, 'Please review your profile details and then upload the required documents.')
            return redirect('applicant:apply', id=id)

    return render(request, 'payment/verify-payment', title='BSSB Verify Payment')