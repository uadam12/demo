from django.shortcuts import get_object_or_404
from app import render
from app.views import update_view, delete_view, create_view
from app.auth import officials_only
from .forms import (
    InstitutionType, InstitutionTypeForm,
    Institution, InstitutionForm,
    CourseType, CourseTypeForm,
    Program, ProgramForm,
    Course, CourseForm,
    Level, LevelForm
)


# Institution Types
@officials_only()
def institution_types(request):
    return render(
        request, "academic/institution-types",
        title='BSSB | Institution Types',
        institution_types = InstitutionType.objects.all()
    )

def institution_type(request):
    id = request.GET.get('institution_type')
    institution_type = get_object_or_404(InstitutionType, id=id)
    institutions = institution_type.institutions.all()
    
    return render(request, 'parts/options', data = institutions, empty_label=f'Select your {institution_type}')

@officials_only(admin_only=True)
def create_institution_type(request):
    return create_view(
        request, form_class=InstitutionTypeForm, 
        success_url='academic:institution-types', 
        header='Create Institution Type'
    )

@officials_only(admin_only=True)
def update_institution_type(request, id):
    institution_type = get_object_or_404(InstitutionType, id=id)
    
    return update_view(
        request, instance=institution_type, 
        form_class=InstitutionTypeForm, 
        success_url='academic:institution-types', 
        header=f'Update {institution_type}'
    )

@officials_only(admin_only=True)
def delete_institution_type(request, id):
    institution_type = get_object_or_404(InstitutionType, id=id)
    
    return delete_view(
        request, model=institution_type,
        success_url='academic:institution-types', 
        header='Delete Institution Type'
    )

# Institutions
@officials_only()
def institutions(request):
    return render(
        request, "academic/institutions",
        title='BSSB | Institutions',
        institutions = Institution.objects.all(),
    )

@officials_only(admin_only=True)
def create_institution(request):
    return create_view(
        request, form_class=InstitutionForm, 
        success_url='academic:institutions', 
        header='Create Institution'
    )

@officials_only(admin_only=True)
def update_institution(request, id):
    institution = Institution.objects.get(id=id)

    return update_view(
        request, 
        instance=institution, 
        form_class=InstitutionForm, 
        success_url='academic:institutions', 
        header='Update Institution'
    )
    
@officials_only(admin_only=True)
def delete_institution(request, id):
    institution = Institution.objects.get(id=id)
    
    return delete_view(
        request, model=institution,
        success_url='academic:institutions', 
        header='Delete Institution'
    )


# Programs
@officials_only()
def programs(request):
    return render(
        request, "academic/programs",
        title='BSSB | Institutions',
        programs = Program.objects.all(),
    )

def program(request):
    id = request.GET.get('program')
    program = get_object_or_404(Program, id=id)
    levels = program.levels.all()
    
    return render(request, 'parts/options', data = levels, empty_label='Select your current level')

@officials_only(admin_only=True)
def create_program(request):
    return create_view(
        request, form_class=ProgramForm, 
        success_url='academic:programs', 
        header='Create Program'
    )

@officials_only(admin_only=True)
def update_program(request, id):
    program = get_object_or_404(Program, id=id)
    
    return update_view(
        request, instance=program, 
        form_class=ProgramForm, 
        success_url='academic:programs', 
        header='Delete Program'
    )


@officials_only(admin_only=True)    
def delete_program(request, id):
    program = get_object_or_404(Program, id=id)

    return delete_view(
        request, model=program,
        success_url='academic:programs', 
        header='Delete Program'
    )

# Course types
@officials_only()
def course_types(request):
    return render(
        request, "academic/course-types",
        title='BSSB | Course Types',
        course_types = CourseType.objects.all(),
    )

def course_type(request):
    id = request.GET.get('course_type')
    program = get_object_or_404(CourseType, id=id)
    courses = program.courses.all()
    
    return render(request, 'parts/options', data = courses, empty_label='Select your course of study')

@officials_only(admin_only=True)
def create_course_type(request):
    return create_view(
        request, form_class=CourseTypeForm, 
        success_url='academic:course-types', 
        header='Create Course Type'
    )

@officials_only(admin_only=True)
def update_course_type(request, id):
    course_type = get_object_or_404(CourseType, id=id)
    
    return update_view(
        request, instance=course_type, 
        form_class=CourseTypeForm, 
        success_url='academic:course-types', 
        header='Update Course Type'
    )

@officials_only(admin_only=True)
def delete_course_type(request, id):
    course_type = get_object_or_404(CourseType, id=id)
    
    return delete_view(
        request, model=course_type,
        success_url='academic:course-types', 
        header='Delete Course Type'
    )

# Courses
@officials_only()
def courses(request):
    return render(
        request, "academic/courses",
        title='BSSB | Courses',
        courses = Course.objects.all(),
    )

@officials_only(admin_only=True)
def create_course(request):
    return create_view(
        request, form_class=CourseForm, 
        success_url='academic:courses', 
        header='Create Course'
    )

@officials_only(admin_only=True)
def update_course(request, id):
    course = get_object_or_404(Course, id=id)
    
    return update_view(
        request, instance=course, 
        form_class=CourseForm, 
        success_url='academic:courses', 
        header='Update Course'
    )

@officials_only(admin_only=True)
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    
    return delete_view(
        request, model=course,
        success_url='academic:courses', 
        header='Delete Course'
    )
    
# Levels
@officials_only()
def levels(request):
    return render(
        request, "academic/levels",
        title='BSSB | Levels',
        levels = Level.objects.all(),
    )

@officials_only(admin_only=True)
def create_level(request):
    return create_view(
        request, form_class=LevelForm, 
        success_url='academic:levels', 
        header='Create Level'
    )

@officials_only(admin_only=True)
def update_level(request, id):
    level = get_object_or_404(Level, id=id)
    
    return update_view(
        request, instance=level, 
        form_class=LevelForm, 
        success_url='academic:levels', 
        header='Update Level'
    )

@officials_only(admin_only=True)
def delete_level(request, id):
    level = get_object_or_404(Level, id=id)
    
    return delete_view(
        request, model=level,
        success_url='academic:levels', 
        header='Delete Level'
    )