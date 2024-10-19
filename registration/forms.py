from django import forms
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Div, Submit
from crispy_forms.bootstrap import InlineCheckboxes
from board.models import Criterion, Requirement
from .models import Registration

class RegistrationForm(forms.ModelForm):
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

        self.instance = Registration.load()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'fee', 
            InlineCheckboxes('criteria', css_class='criteria'),
            InlineCheckboxes('requirements', css_class='criteria'),
            Div(
                Submit('save', 'Save Registration FEE'), 
                css_class='text-end'
            )
        )
    
    class Meta:
        model = Registration
        fields = ("fee", "criteria", "requirements")
