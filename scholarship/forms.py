from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from crispy_forms.bootstrap import InlineCheckboxes
from app import get_or_none
from board.models import Criterion, Requirement
from academic.models import Institution, Program
from .models import Scholarship, ScholarshipProgram, ApplicationDocument, Application

class DateInput(forms.DateInput):
    input_type = 'date'

class ScholarshipForm(forms.ModelForm):
    criteria = forms.ModelMultipleChoiceField(
        queryset=Criterion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    requirements = forms.ModelMultipleChoiceField(
        queryset=Requirement.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].widget.attrs['placeholder'] = 'Enter Scholarship title'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Scholarship purpose, seperete paragraphs with new line'
        self.fields['application_fee'].widget.attrs['placeholder'] = 'Enter Scholarship Application FEE'
        self.fields['application_commence'].widget = DateInput(attrs={
            'required': True,
            'title': 'Select application commencement date'
        })
        self.fields['application_deadline'].widget = DateInput(attrs={
            'required': True,
            'title': 'Select application deadline date'
        })
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('application_fee', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('application_commence', css_class='form-group col-md-6 mb-0'),
                Column('application_deadline', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            InlineCheckboxes('criteria', css_class='checkbox-columns'),
            InlineCheckboxes('requirements', css_class='checkbox-columns'),
            'description',
            Div(
                Submit('save', 'Save Scholarship'),
                css_class='text-end'
            )
        )
        
    class Meta:
        model = Scholarship
        exclude = ("applicants", "programs")


class ScholarshipProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.scholarship = kwargs.pop('scholarship', None)
        super().__init__(*args, **kwargs)
        
        self.fields['program'].empty_label = 'Select Program'
        self.fields['disbursement_amount'].widget.attrs['placeholder'] = 'Enter disbursement amount per applicant'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'program', 'disbursement_amount',
            Div(
                Submit('save', 'Save Program'),
                css_class='text-end'
            )
        )
        
    def save(self, commit:bool=True) -> ScholarshipProgram:
        if self.scholarship:
            scholarship_program = super().save(commit=False)
            scholarship_program.scholarship = self.scholarship
            if commit: scholarship_program.save()
            return scholarship_program

        return super().save(commit=commit)
    
    class Meta:
        model = ScholarshipProgram
        exclude = ("scholarship", )


class ApplicationForm(forms.Form):
    def __init__(self, application:Application, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.instance = application
        self.documents_fieldnames = []

        for requirement in application.scholarship.requirements.all():
            document = get_or_none(ApplicationDocument, requirement=requirement)
            fieldname = f"application_document_{requirement.pk}"

            self.fields[fieldname] = forms.ImageField(
                label=requirement.text,
                required=requirement.is_compulsory and document is None
            )

            self.documents_fieldnames.append(fieldname)
            
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_id = 'document_form'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            *self.documents_fieldnames,
            Div(
                Submit('upload', 'Apply Now'),
                css_class='text-end'
            )
        )
    
    def save(self):
        for field_name in self.documents_fieldnames:
            image = self.cleaned_data.get(field_name)
            if image:
                id = int(field_name.split('_')[2])
                document, _ = ApplicationDocument.objects.get_or_create(
                    application = self.instance,
                    requirement_id = id
                )
                
                document.image = image
                document.save()

        return True