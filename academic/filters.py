import django_filters as df
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from .models import Course, CourseType, Program, Level, Institution, InstitutionType

class InstitutionFilter(df.FilterSet):
    class Mete:
        model = Institution
        fields = []

    institution_type = df.ModelChoiceFilter(
        field_name = 'institution_type',
        label = 'Institution Type',
        empty_label = 'Select Institution Type',
        queryset = InstitutionType.objects.all(),
    )
    
    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.layout = Layout(
            Row(
                Column('institution_type', css_class='form-group col-md-9'),
                Column(
                    Div(
                        Submit('', "Filter Institutions"), css_class='text-end',
                    ),
                    css_class='form-group col-md-3 mb-0 align-self-end pb-3'
                )
            )
        )
        
        return form
    
class LevelFilter(df.FilterSet):
    class Mete:
        model = Level
        fields = []

    program = df.ModelChoiceFilter(
        field_name = 'program',
        label = 'Academic Program',
        empty_label = 'Select Program',
        queryset = Program.objects.all(),
    )
    
    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.layout = Layout(
            Row(
                Column('program', css_class='form-group col-md-9'),
                Column(
                    Div(
                        Submit('', "Filter Levelss"), css_class='text-end',
                    ),
                    css_class='form-group col-md-3 mb-0 align-self-end pb-3'
                )
            )
        )
        
        return form

class CourseFilter(df.FilterSet):
    class Mete:
        model = Course
        fields = []

    course_type = df.ModelChoiceFilter(
        field_name = 'course_type',
        label = 'Field of study',
        empty_label = 'Select Course Type',
        queryset = CourseType.objects.all(),
    )
    
    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.layout = Layout(
            Row(
                Column('course_type', css_class='form-group col-md-9'),
                Column(
                    Div(
                        Submit('', "Filter Courses"), css_class='text-end',
                    ),
                    css_class='form-group col-md-3 mb-0 align-self-end pb-3'
                )
            )
        )
        
        return form