from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from .models import Article, Contact

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs['placeholder'] = 'Enter article headline here...'
        self.fields['content'].widget.attrs['placeholder'] = 'Enter article content here...'
        
        self.helper = FormHelper()
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('headline', css_class='form-group col-md-6 mb-0'),
                Column('headline_image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'content',
            Div(
                Submit('save', 'Save Article'), 
                css_class='text-end'
            )
        )
        
    class Meta:
        model = Article
        fields = ("headline", "headline_image", "content",)

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter your name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
        self.fields['subject'].widget.attrs['placeholder'] = 'Enter Subject of the message'
        self.fields['body'].widget.attrs['placeholder'] = 'Enter body of the message'
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'subject', 'body',
            Div(
                Submit('send', "Contact us now"),
                css_class='text-end'
            )
        )
    
    class Meta:
        model = Contact
        fields = ("name", "email", "subject", "body")
