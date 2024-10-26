from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from crispy_forms.helper import FormHelper

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email address', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email to reset your password'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            Div(
                Submit('reset', 'Reset'),
                css_class='text-end'
            )
        )

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['password'].widget.attrs['placeholder'] = 'Enter new and also strong password'
        self.fields['confirm'].widget.attrs['placeholder'] = 'Confirm your password'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                Column('confirm', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Div(
                Submit('reset', 'Reset your Password'),
                css_class='text-end'
            )
        )

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('picture', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'picture',
            Div(
                Submit('save', 'Update Your Profile Picture'),
                css_class='text-end'
            )
        )
class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your firstname'
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your lastname'
        self.fields['last_name'].widget.attrs['required'] = True
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            )
        )


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your firstname here...'
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your lastname here...'
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address here...'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create strong password here...'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password here...'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            'email',
            
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )


class UserAddForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', )

class UserEditForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', )

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={
        'required': True,
        'placeholder': 'Enter your email address here...'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': True,
        'placeholder': 'Enter your password here...'
    }))
