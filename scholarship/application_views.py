from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from app import render, is_post, get_or_none
from app.auth import login_required, officials_only
from app.pdf import generate_application_form
from .models import Scholarship, Application
from .filters import ApplicationFilter, DisbursementFilter

@officials_only()
def applications(request):
    scholarships = Scholarship.objects.all()
    
    return render(
        request, 'application/index',
        title='Scholarship Applications',
        scholarships = scholarships
    )


@officials_only()
def scholarship_applications(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    filter = ApplicationFilter(request.GET, queryset=scholarship.applications.all())
    
    return render(
        request, 'scholarship/applications',
        title='Scholarship Applications',
        scholarship = scholarship,
        applications = filter.qs,
        form = filter.form
    )
    
@officials_only()
def scholarship_applications(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    applications = scholarship.applications.exclude(disbursement_status='Paid').all()
    
    if is_post(request):
        applications = applications.filter(status='approved').all()
        
        for application in applications:
            application.disbursement_status='Paid'
            application.save()
        
        messages.success(request, 'Applications disbursed successfully')

    filter = ApplicationFilter(request.GET, queryset=applications)

    return render(
        request, 'scholarship/applications',
        title='Scholarship Applications',
        scholarship = scholarship,
        applications = filter.qs,
        form = filter.form
    )

@officials_only()
def scholarship_disbursements(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    filter = DisbursementFilter(
        request.GET, 
        queryset=scholarship.applications.filter(disbursement_status='Paid').all()
    )

    return render(
        request, 'scholarship/disbursements',
        title='Scholarship Disbursements',
        scholarship = scholarship,
        applications = filter.qs,
        form = filter.form
    )

def approve_application(request, id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    application:Application = get_or_none(Application, id=id)
    
    if application is not None:
        application.status = 'approved'
        application.save()

    return render(request, 'parts/application-status', application=application)

def reject_application(request, id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    application:Application = get_or_none(Application, id=id)
    
    if application is not None:
        application.status = 'rejected'
        application.save()

    return render(request, 'parts/application-status', application=application)


@login_required
def application(_, application_id):
    application = get_object_or_404(Application, application_id=application_id)
    application_form = generate_application_form(application)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{application.application_id} Application Form.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    response.write(application_form)
    
    return response