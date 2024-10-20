import django_filters as df
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from board.models import LGA, Bank
from academic.models import Institution, Program, Course
from users.models import User


class ApplicantFilter(df.FilterSet):
    class Mete:
        model = User
        fields = []

    lga = df.ModelChoiceFilter(
        field_name = 'personal_info__local_government_area',
        label = 'Local Government Area',
        empty_label = 'Select Local Government Area',
        queryset = LGA.objects.all(),
    )
    
    gender = df.ChoiceFilter(
        field_name = 'personal_info__gender',
        label = 'Local Government Area',
        empty_label = 'Select Gender',
        choices = (
            ('Male', 'Male'),
            ('Female', 'Female')
        )
    )
    
    institution = df.ModelChoiceFilter(
        field_name = 'academic_info__institution',
        label = 'Academic Institution',
        empty_label = 'Select Academic Institution',
        queryset = Institution.objects.all(),
    )
    
    program = df.ModelChoiceFilter(
        field_name = 'academic_info__program',
        empty_label = 'Select Program',
        label = 'Program',
        queryset = Program.objects.all(),
    )
    
    course = df.ModelChoiceFilter(
        field_name = 'academic_info__course_of_study',
        empty_label = 'Select Course of Study',
        label = 'Academic Institution',
        queryset = Course.objects.all(),
    )
    
    bank = df.ModelChoiceFilter(
        field_name = 'account_bank__bank',
        empty_label = 'Select Bank',
        label = 'Account Bank',
        queryset = Bank.objects.all(),
    )

    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.layout = Layout(
            Row(
                Column('lga', css_class='form-group col-md-4 mb-0'),
                Column('gender', css_class='form-group col-md-4 mb-0'),
                Column('bank', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('institution', css_class='form-group col-md-4 mb-0'),
                Column('program', css_class='form-group col-md-4 mb-0'),
                Column('course', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Div(
                Submit('filter', "Filter Applicants"),
                css_class='text-end'
            )
        )
        
        return form
    