from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from .models import InstitutionType, Institution, Program, Course, Level

 
class InstitutionTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Institution Type Name'

    class Meta:
        model = InstitutionType
        fields = ("name", )
   
    
class InstitutionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstitutionForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Institution Name'
        self.fields['institution_type'].empty_label = 'Select Type of the Institution'
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'institution_type', 'name',
            Div(
                Submit('save', "Save Institution"),
                css_class='text-end'
            )
        )

    class Meta:
        model = Institution
        fields = ("name", "institution_type")


class ProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgramForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Program Name'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            Div(
                Submit('save', "Save Program"),
                css_class='text-end'
            )
        )

    class Meta:
        model = Program
        fields = ("name", )

class LevelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LevelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Level Name'
        self.fields['code'].widget.attrs['placeholder'] = 'Enter Level Code'
        self.fields['program'].empty_label = 'Select Program'
    
    class Meta:
        model = Level
        fields = ("name", "code", "program")


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Enter Course Title'
        self.fields['program'].empty_label = 'Select program'

    class Meta:
        model = Course
        fields = ("title", "program")
