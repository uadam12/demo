from django.shortcuts import get_object_or_404
from django.urls import reverse
from app import render
from app.views import delete_view, create_view, update_view, data_view
from app.auth import officials_only
from .models import ApplicationDocument
from .forms import ScholarshipForm, Scholarship, ApplicationDocumentForm
from .filters import FilterScholarship


# Create your views here.
@officials_only()
def index(request):
    filter = FilterScholarship(request.GET, queryset=Scholarship.objects.all())

    return data_view(
        request=request, 
        title='Scholarships',
        add_url=reverse('scholarship:create'),
        data_template='scholarship/index.html', 
        data = filter.qs, filter_form=filter.form,
        table_headers=[
            'S/N', "Name", 'Application Commence', 
            'Application Deadline', 'Actions'
        ]
    )


@officials_only()
def scholarship(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    return render(
        request, 'scholarship/info',
        scholarship = scholarship,
        title=f"{scholarship} details",
        data_template='board/reg-documents.html',
        with_htmx=True, with_modal=True,
        table_headers=['S/N', 'Name', 'Is Compulsory', 'Actions'],
        data_url=reverse('scholarship:app-documents', kwargs={'id': id}),
        add_url=reverse('scholarship:create-app-document', kwargs={'id': id})
    )

# Application Documents
def app_docuements(request, id):
    return data_view(
        request, data=ApplicationDocument.objects.all(),
        data_template='board/reg-documents.html',
        table_headers=['S/N', 'Name', 'Is Compulsory', 'Actions'],
        add_url=reverse('scholarship:create-app-document', kwargs={'id': id}),
        title='Application Documents'
    )
    
def create_app_docuement(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    def save(app_doc:ApplicationDocument):
        app_doc.scholarship = scholarship
        app_doc.save()
    
    return create_view(
        request, form_class=ApplicationDocumentForm, 
        save_instantly=False, further_action=save,
        success_url='scholarship:app-documents', 
        form_header='Create Application Document',
    )

def update_app_document(request, id):
    app_doc = get_object_or_404(ApplicationDocument, id=id)
    
    return update_view(
        request, ApplicationDocumentForm, 
        app_doc, "Update Application Document", 
        save_instantly=True
    )

def delete_app_document(request, id):
    app_doc = get_object_or_404(ApplicationDocument, id=id)
    
    return delete_view(
        request, app_doc, "Delete Application Document"
    )

# Scholarship
@officials_only(main_admin_only= not True)
def create_scholarship(request):
    return create_view(
        request, 
        form_header='Create Scholarship',
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
        #form_class=ScholarshipProgramForm,
        form_kwargs={
            'scholarship': scholarship
        }, 
        success_url=reverse('scholarship:scholarship', kwargs={'id': id})
    )

@officials_only(main_admin_only=True)
def update_scholarship_program(request, id):
    program = None#get_object_or_404(ScholarshipProgram, id=id)
    
    return update_view(
        request, 
        header='Update Scholarship Program',
        instance=program,
        #form_class=ScholarshipProgramForm,
        form_kwargs={
            'scholarship': program.scholarship
        }, 
        success_url=reverse('scholarship:scholarship', kwargs={'id': id})
    )

@officials_only(main_admin_only=True)
def delete_scholarship_program(request, id):
    program = None#get_object_or_404(ScholarshipProgram, id=id)
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
