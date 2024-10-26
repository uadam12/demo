from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit, Field
from app import get_or_none
from registration.models import Registration, Document
from academic.models import Institution, Level, Course
from .models import PersonalInformation, AcademicInformation, AccountBank, Referee

class DateInput(forms.DateInput):
    input_type = 'date'


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['guardian_name'].widget.attrs['placeholder'] = 'Enter guardian name here...'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number here...'
        self.fields['date_of_birth'].widget = DateInput(attrs={
            'required': True,
            'title': 'Select your date of birth'
        })
        self.fields['place_of_birth'].widget.attrs['placeholder'] = 'Enter place of birth here...'
        self.fields['bvn'].widget.attrs['placeholder'] = 'Enter bank varification number here...'
        self.fields['nin'].widget.attrs['placeholder'] = 'Enter national identification number here...'
        self.fields['local_government_area'].empty_label = 'Select Local Government Area'
        self.fields['residential_address'].widget.attrs['placeholder'] = 'Enter contact address here...'

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('gender', css_class='form-group col-md-4 mb-0'),
                Column('guardian_name', css_class='form-group col-md-4 mb-0'),
                Column('phone_number', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            
            Row(
                Column('date_of_birth', css_class='form-group col-md-6 mb-0'),
                Column('place_of_birth', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            Row(
                Column('bvn', css_class='form-group col-md-6 mb-0'),
                Column('nin', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            Row(
                Column('local_government_area', css_class='form-group col-md-6 mb-0'),
                Column('residential_address', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            )
        )


class AcademicInformationForm(forms.ModelForm):
    class Meta:
        model = AcademicInformation
        exclude = ('user', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['id_number'].widget.attrs['placeholder'] = 'Enter your ID number here...'
        self.fields['institution_type'].empty_label = 'Select institution type'
        self.fields['institution'].empty_label = 'Please select institution type'
        #self.fields['institution'].queryset = Institution.objects.none()
        self.fields['program'].empty_label = 'Select program'
        self.fields['course_type'].empty_label = 'Select course type'
        self.fields['course_of_study'].empty_label = 'Please select course type'
        #self.fields['course_of_study'].queryset = Course.objects.none()
        self.fields['current_level'].empty_label = 'Please select program'
        #self.fields['current_level'].queryset = Level.objects.none()
        
        self.helper = FormHelper()
        self.helper.attrs['hx-post'] = reverse('applicant:save-academic-info')

        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'institution_type', 
                        hx_get = reverse('academic:institution-type'),
                        hx_trigger = 'change', hx_target='#id_institution'
                    ), 
                    css_class='form-group col-md-6 mb-0',
                ),
                Column('institution', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(Field(
                        'program', 
                        hx_get = reverse('academic:program'),
                        hx_trigger = 'change', hx_target='#id_current_level'
                    ), 
                    css_class='form-group col-md-4 mb-0'
                ),
                Column('current_level', css_class='form-group col-md-4 mb-0'),
                Column('id_number', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(Field(
                        'course_type', 
                        hx_get = reverse('academic:course-type'),
                        hx_trigger = 'change', hx_target='#id_course_of_study'
                    ), 
                    css_class='form-group col-md-6 mb-0'
                ),
                Column('course_of_study', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('year_of_admission', css_class='form-group col-md-6 mb-0'),
                Column('year_of_graduation', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Div(
                Submit('save', 'Save Academic Information'),
                css_class='text-end'
            )
        )


class AccountBankForm(forms.ModelForm):
    
    class Meta:
        model = AccountBank
        exclude = ('user', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['bank'].empty_label = 'Select your bank'
        self.fields['account_number'].widget.attrs['placeholder'] = 'Enter your account number here...'
        self.fields['account_name'].widget.attrs['placeholder'] = 'Enter your account name here...'
        
        self.helper = FormHelper()
        self.helper.attrs['hx-post'] = reverse('applicant:save-bank-info')
        self.helper.layout = Layout(
            Row(
                Column('bank', css_class='form-group col-md-6 mb-0'),
                Column('account_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'account_name',
            Div(
                Submit('save', 'Save Bank Account'),
                css_class='text-end'
            )
        )

class RefereeForm(forms.ModelForm):
    
    class Meta:
        model = Referee
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['fullname'].widget.attrs['placeholder'] = 'Enter referees fullname here...'
        self.fields['occupation'].widget.attrs['placeholder'] = 'Enter occupation here...'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter referees fullname here...'
        
        self.helper = FormHelper()
        self.helper.attrs['hx-post'] = reverse('applicant:save-referee')
        self.helper.layout = Layout(
            'fullname',
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                Column('occupation', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Div(
                Submit('save', 'Save Referee'),
                css_class='text-end'
            )
        )

class DocumentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        
        if self.user is None:
            raise ValueError('User argument is required!!!')

        super().__init__(*args, **kwargs)
    
        registration = Registration.load()
        self.documents_fieldnames = []
        
        for requirement in registration.requirements.all():
            document = get_or_none(Document, owner=self.user, requirement=requirement)
            fieldname = f"registration_document_{requirement.pk}"
            
            self.fields[fieldname] = forms.ImageField(
                label=requirement.text,
                required=requirement.is_compulsory and document is None
            )
            
            self.documents_fieldnames.append(fieldname)
        
        self.helper = FormHelper()
        self.helper.attrs['hx-post'] = reverse('applicant:save-document')
        self.helper.attrs['hx-encoding'] = 'multipart/form-data'
        self.helper.layout = Layout(
            *self.documents_fieldnames,
            Div(
                Submit('save', 'Save Documents'),
                css_class='text-end'
            )
        )
        
    def save(self):
        for field_name in self.documents_fieldnames:
            image = self.cleaned_data.get(field_name)
            if image:
                id = int(field_name.split('_')[2])
                document, _ = Document.objects.get_or_create(
                    owner = self.user,
                    requirement_id = id
                )
                
                document.image = image
                document.save()

        return True