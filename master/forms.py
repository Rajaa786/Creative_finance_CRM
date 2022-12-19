from pyexpat import model
from django.forms import DateField, widgets, ModelForm
from django import forms
from django.forms.models import ModelForm, ModelChoiceField
from django.forms.widgets import EmailInput, NumberInput, TextInput
from .models import *
from account.models import *
from django.db.models import Q
from datetime import *
from master.models import *
from django.db.models import Q


class ProductAndPolicyMasterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductAndPolicyMasterForm, self).__init__(*args, **kwargs)
        self.fields['product_name'] = ModelChoiceField(queryset=Product.objects.all(), empty_label="-- Select Product --")

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Product_and_Policy_Master

        labels = {
            "current_experience": "Current Experience (in months)",
            "is_salary_account": "Salary account in this Bank?",
            "total_experience": "Total Experience (in years)"
        }

        exclude = ('effective_date', 'ineffective_date', 'multiplier_info' , 'foir_info' , 'rate_of_interest' , 'salary_type', 'residence_type', 'tenure', 'company_type')
