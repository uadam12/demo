from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpRequest
from app import render
from app.auth import login_required, officials_only
from app.pdf import generate_application_form
from .models import Scholarship, Application

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
    
    return render(
        request, 'scholarship/applications',
        title='Scholarship Applications',
        scholarship = scholarship
    )

@login_required
def application(request:HttpRequest, application_id):
    application = get_object_or_404(Application, application_id=application_id)
    application_form = generate_application_form(application, request)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="some_file.pdf"'
    response.write(application_form)
    
    return response