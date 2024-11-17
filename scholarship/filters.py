import django_filters as df
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from academic.models import Institution, Program, Course
from board.models import Bank
from .models import Application

class Filter(df.FilterSet):
    class Mete:
        model = Application
        fields = []
    
    application_id = df.CharFilter(
        'application_id', lookup_expr='iexact',
        label='Application ID'
    )

    institution = df.ModelChoiceFilter(
        field_name = 'institution',
        label = 'Academic Institution',
        empty_label = 'Select Academic Institution',
        queryset = Institution.objects.all(),
    )
    
    program = df.ModelChoiceFilter(
        field_name = 'program',
        empty_label = 'Select Program',
        label = 'Program',
        queryset = Program.objects.all(),
    )
    
    course_of_study = df.ModelChoiceFilter(
        field_name = 'course_of_study',
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
            'application_id', 'status', 'bank', 
            'institution', 'program', 'course_of_study',
        )
        form.helper.add_input(Submit('filter', "Filter Applicants"))
        
        return form

class ApplicationFilter(Filter):
    status = df.ChoiceFilter(
        field_name = 'status',
        label = 'Application Status',
        empty_label = 'Select Application Status',
        choices = Application.STATUS
    )
    
class DisbursementFilter(Filter):
    status = df.ChoiceFilter(
        field_name = 'disbursement_status',
        label = 'Disbursement Status',
        empty_label = 'Select Disbursement Status',
        choices = Application.DISBURSEMENT_STATUS
    )