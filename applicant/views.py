import json
from django.shortcuts import  get_object_or_404, redirect
from django.template.context_processors import csrf
from django.http import HttpResponse
from django.contrib import messages
from crispy_forms.utils import render_crispy_form
from applicant.models import Referee
from users.forms import ProfilePictureForm
from app import is_post, get_or_none, render
from app.auth import applicant_only
from scholarship.models import Scholarship
from scholarship.forms import ApplicationForm, Application
from payment.models import ApplicationFEE
from payment.remita import remita
from .forms import (
    PersonalInformationForm, PersonalInformation,
    AcademicInformationForm, AcademicInformation,
    AccountBankForm, AccountBank, RefereeForm,
    SchoolAttendedForm, SchoolAttended,
    DocumentForm, Document
)

def render_form(request, form):
    ctx = {}
    ctx.update(csrf(request))
    return HttpResponse(render_crispy_form(form, context=ctx))


# Create your views here.
@applicant_only
def dashboard(request):
    applications = request.user.applications.all()
    return render(
        request, 'applicants/dashboard', 
        applications = applications,
        title = 'BSSB Dashboard', 
    )

@applicant_only
def change_profile_picture(request):
    if is_post(request):
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and form.save():
            messages.success(request, 'Profile picture updated successfully!!!')
            return render(request, 'parts/profile-img')

    messages.error(request, 'Invalid request')
    return HttpResponse(status=204)

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
        applicant_form = PersonalInformationForm(instance=applicant),
        academic_form = AcademicInformationForm(instance=academic_info),
        profile_picture_form = ProfilePictureForm(instance=request.user),
        bank_form = AccountBankForm(instance=account_bank),
        referee_form = RefereeForm(instance=referee),
        schools = SchoolAttended.objects.filter(user=request.user),
        document_form = DocumentForm(user=user),
        documents = documents, with_htmx = True,
    )

@applicant_only
def personal_information(request):
    form = PersonalInformation()

    if is_post(request):
        info = get_or_none(PersonalInformation, user=request.user)
        form = PersonalInformationForm(request.POST, instance=info)

        if form.is_valid():
            info = form.save(False)
            info.user = request.user
            info.save()

            messages.success(request, 'Personal Information save successfully.')
    return render_form(request, form)


@applicant_only
def academic_information(request):
    form = AcademicInformationForm()

    if is_post(request):
        info = get_or_none(AcademicInformation, user=request.user)
        form = AcademicInformationForm(request.POST, instance=info)

        if form.is_valid():
            info = form.save(False)
            info.user = request.user
            info.save()
            
            messages.success(request, "Academic Information Save successfully.")
    return render_form(request, form)

@applicant_only
def account_details(request):
    form = AccountBankForm()

    if is_post(request):
        account_bank = get_or_none(AccountBank, user=request.user)
        form = AccountBankForm(request.POST, instance=account_bank)

        if form.is_valid():
            bvn = request.user.personal_info.bvn
            bank_code = form.cleaned_data['bank']
            account_number = form.cleaned_data['account_number']
            
            account_details = remita.get_account_details(bvn, bank_code, account_number)

            if account_details.get('valid'):
                account_name = account_details.get('nameOnAccount')
                account_bank:AccountBank = form.save(False)
                account_bank.account_name = account_name
                account_bank.user = request.user
                account_bank.save()
                messages.success(request, "Account bank details Save successfully.")
                messages.info(request, f"Account name: {account_name}")
            else: messages.error(request, account_details.get('message'))

    return render_form(request, form)

@applicant_only
def schools_attended(request):
    schools = SchoolAttended.objects.filter(user=request.user).all()
    return render(request, 'parts/schools-attended', schools=schools)

@applicant_only
def add_school(request):
    form = SchoolAttendedForm()
    
    if is_post(request):
        form = SchoolAttendedForm(request.POST)
        if form.is_valid():
            school = form.save(False)
            school.user = request.user
            school.save()

            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'schoolListChanged'
            
            messages.success(request, f"{school} added.")
            return response

    return render(request, 'parts/school-form', form=form, modal_header='Add School Attended')

@applicant_only
def update_school(request, pk):
    school = get_object_or_404(SchoolAttended, pk=pk)
    form = SchoolAttendedForm(instance=school)
    
    if is_post(request):
        form = SchoolAttendedForm(request.POST, instance=school)
        if form.is_valid():
            school = form.save(False)
            school.user = request.user
            school.save()

            messages.success(request, f"{school} updated successfully.")
            response = HttpResponse(status=204)
            response['HX-Trigger'] = 'schoolListChanged'
            return response

    return render(request, 'parts/school-form', form=form, modal_header='Update School Attended')

@applicant_only
def delete_school(request, pk):
    school = get_object_or_404(SchoolAttended, pk=pk)
    
    if is_post(request):
        school.delete()
        messages.success(request, f"{school} deleted.")
        return HttpResponse(status=204)


    return render(request, 'parts/delete-school-confirmation', school=school)

@applicant_only
def documents(request):
    form = DocumentForm(user=request.user)

    if is_post(request):
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid() and form.save():
            messages.success(request, "Registration documents uploaded successfully!!!")
    
    return render_form(request, form)

@applicant_only
def referees(request):
    form = RefereeForm()

    if is_post(request):
        referee = get_or_none(Referee, user=request.user)
        form = RefereeForm(request.POST, instance=referee)
        
        if form.is_valid(): 
            referee = form.save(False)
            referee.user = request.user
            referee.save()

            messages.success(request, "Referee Save successfully.")
    

    return render_form(request, form)

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
        title=f"Application for {scholarship}"
    )