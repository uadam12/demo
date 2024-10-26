import django_filters as df
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from .models import Payment

class PaymentFilter(df.FilterSet):
    class Mete:
        model = Payment
        fields = []

    payment_type = df.ChoiceFilter(
        field_name = 'code',
        label = 'Payment Type',
        empty_label = 'Select Payment Type',
        choices = Payment.TYPES
    )
    
    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_method = 'get'
        form.helper.layout = Layout(
            Row(
                Column('payment_type', css_class='form-group col-md-9'),
                Column(
                    Div(
                        Submit('', "Filter Payments"), css_class='text-end',
                    ),
                    css_class='form-group col-md-3 mb-0 align-self-end pb-3'
                )
            )
        )
        
        return form