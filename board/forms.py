from django import forms
from crispy_forms.layout import Layout, Submit, Div, Row, Column
from crispy_forms.helper import FormHelper
from .models import Criterion, Requirement, Bank, LGA


class CriterionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CriterionForm, self).__init__(*args, **kwargs)
        
        self.fields['text'].widget.attrs['Placeholder'] = 'Enter Criterion text here...'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'text',
            Div(
                Submit('save', 'Save Criterion'), 
                css_class='text-end'
            )
        )
    
    class Meta:
        model = Criterion
        fields = ("text",)

class RequirementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        
        self.fields['text'].widget.attrs['Placeholder'] = 'Enter Criterion text here...'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'text', 'is_compulsory',
            Div(
                Submit('save', 'Save Requirement'), 
                css_class='text-end'
            )
        )
    
    class Meta:
        model = Requirement
        fields = ("text", "is_compulsory")

class BankForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BankForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Bank Name here...'
        self.fields['code'].widget.attrs['placeholder'] = 'Enter Bank Code here...'
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'is_available',
            Div(
                Submit('save', 'Save Bank'), 
                css_class='text-end'
            )
        )
        
        
    class Meta:
        model = Bank
        fields = ("name", "code", "is_available")

class LGAForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LGAForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Local Goverment Area Name here...'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name', 'code',
            Div(Submit('save', 'Save LGA'), css_class='text-end')
        )

    class Meta:
        model = LGA
        fields = ("name", "code")
