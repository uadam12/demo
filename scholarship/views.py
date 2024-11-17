from django.shortcuts import get_object_or_404
from django.urls import reverse
from app import render
from app.views import delete_view, create_view, update_view
from app.auth import officials_only
from .forms import ScholarshipForm, Scholarship, ScholarshipProgramForm, ScholarshipProgram


# Create your views here.
@officials_only()
def index(request):
    return render(
        request, 'scholarship/index',
        title='BSSB | All Scholarships',
        scholarships=Scholarship.objects.all(),
    )

@officials_only()
def scholarship(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    return render(
        request, 'scholarship/info',
        scholarship = scholarship,
        title=f"{scholarship} details"
    )

@officials_only(main_admin_only=True)
def create_scholarship(request):
    return create_view(
        request, 
        header='Create Scholarship',
        form_class=ScholarshipForm, 
        success_url='scholarship:index'
    )


@officials_only(main_admin_only=True)
def update_scholarship(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    return update_view(
        request, 
        instance=scholarship,
        header=f'Update {scholarship}',
        form_class=ScholarshipForm, 
        success_url=reverse('scholarship:scholarship', kwargs={'id': id})
    )
    
@officials_only(main_admin_only=True)
def delete_scholarship(request):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    return delete_view(
        request, 
        instance=scholarship,
        header=f'BSSB Delete {scholarship}',
        success_url=reversed('scholarship:index')
    )


@officials_only(main_admin_only=True)
def add_scholarship_program(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    return create_view(
        request, 
        header='Create Scholarship Program',
        form_class=ScholarshipProgramForm,
        form_kwargs={
            'scholarship': scholarship
        }, 
        success_url=reverse('scholarship:scholarship', kwargs={'id': id})
    )

@officials_only(main_admin_only=True)
def update_scholarship_program(request, id):
    program = get_object_or_404(ScholarshipProgram, id=id)
    
    return update_view(
        request, 
        header='Update Scholarship Program',
        instance=program,
        form_class=ScholarshipProgramForm,
        form_kwargs={
            'scholarship': program.scholarship
        }, 
        success_url=reverse('scholarship:scholarship', kwargs={'id': id})
    )

@officials_only(main_admin_only=True)
def delete_scholarship_program(request, id):
    program = get_object_or_404(ScholarshipProgram, id=id)
    scholarship_id = program.scholarship.id
    
    return delete_view(
        request=request,
        model=program,
        success_url=reverse('scholarship:scholarship', kwargs={'id': scholarship_id})
    )


@officials_only()
def internal_scholarships(request):
    internal = get_object_or_404(Scholarship, id=id)
    
    return render(
        request, 'scholarship/internals', 
        title=f"BSSB {internal}", 
        scholarship=internal.scholarship,
        internal = internal
    )

@officials_only()
def internal_scholarships(request):
    return render(
        request, 'scholarship/externals',
        title='BSSB | External Scholarships',
    )
    

@officials_only()
def external_scholarships(request):
    return render(
        request, 'scholarship/externals',
        title='BSSB | External Scholarships',
    )
