from django.shortcuts import get_object_or_404
from django.urls import reverse
from app import render
from app.views import update_view, delete_view, create_view, data_view
from app.auth import officials_only
from .filters import (
    CourseFilter, LevelFilter, InstitutionFilter, 
    ProgramFilter, InstitutionTypeFilter
)
from .forms import (
    InstitutionType, InstitutionTypeForm,
    Institution, InstitutionForm,
    Program, ProgramForm,
    Course, CourseForm,
    Level, LevelForm
)


# Institution Types
@officials_only()
def institution_types(request):
    filter = InstitutionTypeFilter(request.GET, queryset=InstitutionType.objects.all())
    return data_view(
        request, title='Institution Types',
        data_template="academic/institution-types.html",
        table_headers=['S/N', 'Name', 'Action'], filter_form=filter.form,
        data=filter.qs, add_url=reverse('academic:create-institution-type')
    )

def institution_type(request):
    id = request.GET.get('institution_type')
    
    if not id:
        return render(request, 'parts/options', data = Institution.objects.none(), empty_label=f'Select your institution type')
    
    institution_type = get_object_or_404(InstitutionType, id=id)
    institutions = institution_type.institutions.all()
    
    return render(request, 'parts/options', data = institutions, empty_label=f'Select your {institution_type}')

@officials_only(admin_only=True)
def create_institution_type(request):
    return create_view(
        request, form_class=InstitutionTypeForm, 
        success_url='academic:institution-types', 
        form_header='Create Institution Type'
    )

@officials_only(admin_only=True)
def update_institution_type(request, id):
    inst_type = get_object_or_404(InstitutionType, id=id)
    
    return update_view(
        request, instance=inst_type, 
        form_class=InstitutionTypeForm, 
        form_header=f'Update {inst_type}'
    )

@officials_only(admin_only=True)
def delete_institution_type(request, id):
    inst_type = get_object_or_404(InstitutionType, id=id)
    return delete_view(request, model=inst_type, header='Delete Institution Type')

# Institutions
@officials_only()
def institutions(request):
    filter = InstitutionFilter(request.GET, queryset=Institution.objects.all())
    return data_view(
        request, title='Institutions',
        data_template="academic/institutions.html",
        table_headers=['S/N', 'Name', 'Type', 'Action'], filter_form=filter.form,
        data=filter.qs.prefetch_related('institution_type'), add_url=reverse('academic:create-institution')
    )

@officials_only(admin_only=True)
def create_institution(request):
    return create_view(
        request, form_class=InstitutionForm, 
        success_url='academic:institutions', 
        form_header='Create Institution'
    )

@officials_only(admin_only=True)
def update_institution(request, id):
    institution = Institution.objects.get(id=id)

    return update_view(
        request, 
        instance=institution, 
        form_class=InstitutionForm, 
        form_header='Update Institution'
    )
    
@officials_only(admin_only=True)
def delete_institution(request, id):
    institution = Institution.objects.get(id=id)
    
    return delete_view(
        request, model=institution,
        header='Delete Institution'
    )


# Programs
@officials_only()
def programs(request):
    filter = ProgramFilter(request.GET, queryset=Program.objects.all())

    return data_view(request, 
        data_template="academic/programs.html",
        title='Programs', filter_form=filter.form,
        table_headers=['S/N', 'Program Name', 'Action'],
        data=filter.qs, add_url=reverse('academic:create-program')
    )

def program(request):
    id = request.GET.get('program')

    if not id:
        return render(request, 'parts/options', data = Level.objects.none(), empty_label=f'Select your program')

    program = get_object_or_404(Program, id=id)
    levels = program.levels.all()
    
    return render(request, 'parts/options', data = levels, empty_label='Select your current level')

@officials_only(admin_only=True)
def create_program(request):
    return create_view(
        request, form_class=ProgramForm, 
        success_url='academic:programs',
        form_header='Create Program'
    )

@officials_only(admin_only=True)
def update_program(request, id):
    program = get_object_or_404(Program, id=id)
    
    return update_view(
        request, instance=program, 
        form_class=ProgramForm, form_header='Update Program'
    )

@officials_only(admin_only=True)    
def delete_program(request, id):
    program = get_object_or_404(Program, id=id)
    return delete_view(request, model=program, header='Delete Program')

# Courses
@officials_only()
def courses(request):
    filter = CourseFilter(request.GET, queryset=Course.objects.all())
    return data_view(
        request, title='Courses',
        filter_form = filter.form,
        data_template="academic/courses.html",
        add_url=reverse('academic:create-course'),
        data=filter.qs.prefetch_related('program'), 
        table_headers=['S/N', 'Title', 'Program', 'Action']
    )

@officials_only(admin_only=True)
def create_course(request):
    return create_view(
        request, form_class=CourseForm, 
        success_url='academic:courses', 
        form_header='Create Course'
    )

@officials_only(admin_only=True)
def update_course(request, id):
    course = get_object_or_404(Course, id=id)
    
    return update_view(request, instance=course, form_class=CourseForm, form_header='Update Course')

@officials_only(admin_only=True)
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    
    return delete_view(request, model=course, header='Delete Course')
    
# Levels
@officials_only()
def levels(request):
    filter = LevelFilter(request.GET, queryset=Level.objects.all())
    return data_view(
        request, filter_form = filter.form,
        title='Levels', data_template="academic/levels.html",
        table_headers=['S/N', 'Name', 'Code', 'Program', 'Action'],
        data=filter.qs.prefetch_related('program'), add_url=reverse('academic:create-level')
    )

@officials_only(admin_only=True)
def create_level(request):
    return create_view(
        request, form_class=LevelForm, 
        success_url='academic:levels', 
        form_header='Create Level'
    )

@officials_only(admin_only=True)
def update_level(request, id):
    level = get_object_or_404(Level, id=id)
    
    return update_view(
        request, instance=level, 
        form_class=LevelForm, 
        form_header='Update Level'
    )

@officials_only(admin_only=True)
def delete_level(request, id):
    level = get_object_or_404(Level, id=id)
    return delete_view(request, model=level, header='Delete Level')