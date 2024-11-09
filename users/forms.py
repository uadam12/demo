from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from crispy_forms.helper import FormHelper
from app.validators import validate_phone_number

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
    phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    nin = forms.CharField(label="National Identification Number", max_length=11, min_length=11, required=True)
    bvn = forms.CharField(label="Bank Verification Number", max_length=11, min_length=11, required=True)
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['nin'].widget.attrs['placeholder'] = 'Enter your NIN'
        self.fields['bvn'].widget.attrs['placeholder'] = 'Enter your BVN'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create strong password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            Row(
                Column('nin', css_class='form-group col-md-6 mb-0'),
                Column('bvn', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
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
