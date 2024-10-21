import django_filters as df
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from .models import Course, CourseType, Program, Level

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
                Column('course_type', css_class='form-group col-md-9 mb-'),
                Column(
                    Div(
                        Submit('filter', "Filter Courses"), css_class='text-end',
                    ),
                    css_class='form-group col-md-3 mb-0'
                )
            )
        )
        
        return form