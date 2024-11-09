from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit, Field
from app import get_or_none
from registration.models import Registration, Document
from .models import PersonalInformation, AcademicInformation, AccountBank, SchoolAttended, Referee

class DateInput(forms.DateInput):
    input_type = 'date'


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = ('phone_number', 'place_of_birth', 'guardian_name', 'guardian_phone_number', 'residential_address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['guardian_name'].widget.attrs['placeholder'] = 'Enter your guardian name'
        self.fields['guardian_phone_number'].widget.attrs['placeholder'] = 'Enter your guardian phone number'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['place_of_birth'].widget.attrs['placeholder'] = 'Enter your place of birth'
        self.fields['residential_address'].widget.attrs['placeholder'] = 'Enter your residential address'

        self.helper = FormHelper()
        self.helper.attrs['hx-post'] = reverse('applicant:save-personal-info')
        self.helper.attrs['hx-target'] = 'this'
        self.helper.layout = Layout(
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                Column('place_of_birth', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('guardian_name', css_class='form-group col-md-5 mb-0'),
                Column('guardian_phone_number', css_class='form-group col-md-7 mb-0'),
                css_class='form-row'
            ),
            'residential_address',
            Div(
                Submit('save', 'Save Personal Information'),
                css_class='text-end'
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
        self.fields['program'].empty_label = 'Select program'
        self.fields['course_type'].empty_label = 'Select course type'
        self.fields['course_of_study'].empty_label = 'Please select course type'
        self.fields['current_level'].empty_label = 'Please select program'
        
        self.helper = FormHelper()
        self.helper.attrs['hx-post'] = reverse('applicant:save-academic-info')
        self.helper.attrs['hx-target'] = 'this'
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
        self.helper.attrs['hx-target'] = 'this'
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

class SchoolAttendedForm(forms.ModelForm):
    
    class Meta:
        model = SchoolAttended
        exclude = ("user",)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['school_name'].widget.attrs['placeholder'] = 'Enter school attended name'
        self.fields['certificate_obtained'].widget.attrs['placeholder'] = 'Enter certificate obtained from the school'
        self.fields['year_from'].widget.attrs['placeholder'] = 'Enter year you started the school'
        self.fields['year_to'].widget.attrs['placeholder'] = 'Enter year you finished the school'

class RefereeForm(forms.ModelForm):
    
    class Meta:
        model = Referee
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['fullname'].widget.attrs['placeholder'] = 'Enter referees fullname'
        self.fields['occupation'].widget.attrs['placeholder'] = 'Enter referee occupation'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter referees phone number'
        
        self.helper = FormHelper()
        self.helper.attrs['hx-post'] = reverse('applicant:save-referee')
        self.helper.attrs['hx-target'] = 'this'
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
        
        if not hasattr(self, 'instantance') and self.user is None:
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
        self.helper.attrs['hx-target'] = 'this'
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