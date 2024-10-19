from django.shortcuts import  get_object_or_404, redirect
from django.contrib import messages
from applicant.models import Referee
from users.forms import UserForm
from app import is_post, get_or_none, render
from app.auth import applicant_only
from scholarship.models import Scholarship
from scholarship.forms import ApplicationForm, Application
from payment.models import ApplicationFEE
from .forms import (
    PersonalInformationForm, PersonalInformation,
    AcademicInformationForm, AcademicInformation,
    AccountBankForm, AccountBank, RefereeForm,
    DocumentForm, Document
)


# Create your views here.
@applicant_only
def dashboard(request):
    applications = request.user.applications.all()
    return render(request, 'applicants/dashboard', title='BSSB Dashboard', applications=applications)

@applicant_only
def profile(request):
    user = request.user
    applicant = get_or_none(PersonalInformation, user=user)
    academic_info = get_or_none(AcademicInformation, user=user)
    account_bank = get_or_none(AccountBank, user=user)
    referee = get_or_none(Referee, user=user)
    documents = Document.objects.filter(owner=user).all()

    return render(
        request, 'applicants/profile', 
        title='BSSB Applicant Profile',
        user_form = UserForm(instance=request.user),
        applicant_form = PersonalInformationForm(instance=applicant),
        academic_form = AcademicInformationForm(instance=academic_info),
        bank_form = AccountBankForm(instance=account_bank),
        referee_form = RefereeForm(instance=referee),
        document_form = DocumentForm(user=user),
        documents = documents
    )

@applicant_only
def personal_information(request):
    if is_post(request):
        user_form = UserForm(instance=request.user, data=request.POST)
        personal_info = get_or_none(PersonalInformation, user=request.user)
        personal_info_form = PersonalInformationForm(request.POST, instance=personal_info)

        if user_form.is_valid() and personal_info_form.is_valid():
            user_form.save()
            personal_info = personal_info_form.save(False)
            personal_info.user = request.user
            personal_info.save()

            return render(request, 'parts/msg', message='Personal Information Save successfully.')
        return render(request, 'parts/msg', message=str(personal_info_form.errors) + str(user_form.errors))
    
    return render(request, 'parts/msg', message="Invalid Request")


@applicant_only
def academic_information(request):
    if is_post(request):
        academic_info = get_or_none(AcademicInformation, user=request.user)
        form = AcademicInformationForm(request.POST, instance=academic_info)

        if form.is_valid():
            academic_info = form.save(False)
            academic_info.user = request.user
            academic_info.save()
            return render(request, 'parts/msg', message='Academic Information Save successfully.')
        return render(request, 'parts/msg', message=str(form.errors))
    
    return render(request, 'parts/msg', message="Invalid Request")

@applicant_only
def account_details(request):
    if is_post(request):
        account_bank = get_or_none(AccountBank, user=request.user)
        form = AccountBankForm(request.POST, instance=account_bank)
        
        if form.is_valid():
            account_bank = form.save(False)
            account_bank.owner = request.user
            account_bank.save()
            return render(request, 'parts/msg', message='Account details Save successfully.')
        return render(request, 'parts/msg', message=str(form.errors))
    
    return render(request, 'parts/msg', message="Invalid Request")

@applicant_only
def documents(request):
    if is_post(request):
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid() and form.save():
            return render(request, 'parts/msg', message='Registration documents uploaded Save successfully.')
        return render(request, 'parts/msg', message=str(form.errors))
    
    return render(request, 'parts/msg', message="Invalid Request")

@applicant_only
def referees(request):
    if is_post(request):
        referee = get_or_none(Referee, user=request.user)
        form = RefereeForm(request.POST, instance=referee)
        
        if form.is_valid(): 
            referee = form.save(False)
            referee.user = request.user
            referee.save()
            return render(request, 'parts/msg', message='Referee information Save successfully.')
        return render(request, 'parts/msg', message=str(form.errors))
    
    return render(request, 'parts/msg', message="Invalid Request")

@applicant_only
def scholarships(request):
    scholarships = Scholarship.objects.all()
    
    return render(
        request, 'applicants/scholarships', 
        scholarships = scholarships,
        title="Open Scholarships"
    )
    
@applicant_only
def apply(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    applicant_has_paid_application_fee = ApplicationFEE.objects.filter(scholarship=scholarship, applicant=request.user).exists()
    
    if not applicant_has_paid_application_fee:
        return redirect('payment:application-fee', id=id)
    
    application = Application.get_or_create(
        request.user,
        scholarship
    )
    form = ApplicationForm(application)
    
    if is_post(request):
        form = ApplicationForm(application, data=request.POST, files=request.FILES)
        if form.is_valid() and form.save():
            messages.success(request, f'You have successfully applied for {scholarship}')
            return redirect('applicant:dashboard')

    return render(
        request, 'applicants/apply', 
        scholarship = scholarship,
        form = form,
        title="Open Scholarships"
    )