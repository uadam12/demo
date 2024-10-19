from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from crispy_forms.bootstrap import InlineCheckboxes
from .models import InstitutionType, Institution, Program, CourseType, Course, Level

 
class InstitutionTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Institution Type Name'
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            Div(
                Submit('save', "Save Institution Type"),
                css_class='text-end'
            )
        )

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

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'program',
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Div(
                Submit('save', "Save Academic Level"),
                css_class='text-end'
            )
        )
    
    class Meta:
        model = Level
        fields = ("name", "code", "program")


class CourseTypeForm(forms.ModelForm):
    
    class Meta:
        model = CourseType
        fields = ("title", )

class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Enter Course Title'
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Div(
                Submit('save', "Save Academic Program"),
                css_class='text-end'
            )
        )
        
    class Meta:
        model = Course
        fields = ("title", )
