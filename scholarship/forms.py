from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from crispy_forms.bootstrap import InlineCheckboxes
from .models import Scholarship, ApplicationDocument

class DateInput(forms.DateInput):
    input_type = 'date'

class ScholarshipForm(forms.ModelForm):
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


class ApplicationDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ("name", "required")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['placeholder'] = 'Enter application document name'

ApplicationDocumentForms = forms.modelformset_factory(
    ApplicationDocument, form=ApplicationDocumentForm, extra=0
)