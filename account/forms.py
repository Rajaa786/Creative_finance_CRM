from re import M
from typing import Text, Type
from django.forms import DateField, widgets
from django import forms
from django.forms.models import ModelChoiceField, ModelForm
from django.forms.widgets import EmailInput, NumberInput, TextInput
from .models import *
from django.db.models import Q

class LeadsForm(ModelForm):
    class Meta:
        model = Leads
        exclude = ('added_by',)
    def __init__(self, *args, **kwargs):
        super(LeadsForm, self).__init__(*args, **kwargs)
        self.fields['sub_product'].queryset = SubProduct.objects.none() 
        self.fields['city'].queryset = SubProduct.objects.none() 
        self.fields['address'].widget.attrs['rows'] = 1
        self.fields['address'].widget.attrs['columns'] = 40
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
                'autofocus':''
            })

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state = state_id)
            except(ValueError,TypeError):
                pass
        
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['sub_product'].queryset = SubProduct.objects.filter(product = product_id)
            except(ValueError,TypeError):
                pass
        


class TempForm(forms.Form):
    applicant_type = forms.ModelChoiceField(queryset = ApplicantType.objects.filter(~Q(applicant_type = 'Applicant')))
    applicant_type.widget.attrs.update({'class':'form-control','id':'select_applicant_type'})

class AdditionalDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdditionalDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['applicant_type'].widget.attrs.update({'readonly': 'true'})
        self.fields['is_diff'].widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = AdditionalDetails
        exclude = ('lead_id',)

class PropertyDetailsType1Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertyDetailsType1Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = PropType1
        exclude = ('lead_id',)
        widgets = {
            'possession_date': widgets.DateInput(attrs={'type': 'date'})}
        labels = {
            'proj_name':"Project Name",
            'prop_loc':"Property Location",
            'const_stage': "Construction Stage",
            'per_complete':"Percent Complete",
            'prop_city':"Property City",
            'prop_state':"Property State",
            'market_val':"Market Value",
            'cc_rec':"CC Recieved",
            'stamp_duty_amt':"Stamp Duty Amount"
        }


class PropertyType2Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropertyType2Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_data(self):
        cleaned_data = super(PropertyType2Form, self).clean()
        cc_rec = cleaned_data.get('cc_rec')
        cost_sheet = cleaned_data.get('cost_sheet')
        car_parking = cleaned_data.get('car_parking')
        if cc_rec == True:
            if not cleaned_data.get('cc_rec_upto'):
                raise forms.ValidationError("Please enter cc_rec")
        if cost_sheet == True:
            if not cleaned_data.get('cost_sheet_amt'):
                raise forms.ValidationError("Please enter cost_sheet amount")
        if car_parking == True:
            if not cleaned_data.get('car_parking_amt'):
                raise forms.ValidationError("Please enter car parking amt")
    class Meta:
        model = PropType2
        exclude = ('lead_id',)
        widgets = {
            'possession_date': widgets.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'proj_name'      : 'Project Name',
            'prop_loc'       : "Property Location",
            'prop_city'      : "Property City",
            'prop_state'     : "Property State",
            'per_complete'   : 'Percent Complete',
            'const_stage'    : 'Construction Stage',
            'pay_till_date'  : 'Payment Made Till Date',
            'cost_sheet_amt' : 'Cost Sheet Amount',
            'stamp_duty_amt' : 'Stamp Duty Amount',
            'car_parking_amt': 'Car Parking Amount',
            'cc_rec'         : 'CC Recieved'
        }
 


class PropType3Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropType3Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = PropType3
        exclude = ('lead_id',)
        labels = {
            'proj_name'      : 'Project Name',
            'per_complete'   : 'Percent Complete',
            'proj_name'      : 'Project Name',
            'prop_loc'       : "Property Location",
            'prop_city'      : "Property City",
            'prop_state'     : "Property State",
            'const_stage'    : 'Construction Stage',
            'pay_till_date'  : 'Payment Made Till Date',
            'cost_sheet_amt' : 'Cost Sheet Amount',
            'stamp_duty_amt' : 'Stamp Duty Amount',
            'car_parking_amt': 'Car Parking Amount'
        }


class PropType4Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PropType4Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = PropType4
        exclude = ('lead_id',)
        labels = {
            'market_val': "Market Value",
            'prop_loc'  : "Property Location",
            'prop_city' : "Property City",
            'prop_state': "Property State",
            }

class SalIncomeDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalIncomeDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = SalIncomeDetails
        exclude = ('inc_det_id', 'addi_details_id',)


class SalOtherIncomesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalOtherIncomesForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = SalOtherIncomes
        exclude = ('other_inc_id', 'addi_details_id',)
    
class SalAdditionalOtherIncomesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalAdditionalOtherIncomesForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = SalAdditionalOtherIncomes
        exclude = ('add_oth_inc_id', 'addi_details_id',)


# class ContactPersonForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ContactPersonForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})

#     class Meta:
#         model = ContactPerson
#         exclude = ('con_id', 'add_det_id',)


class SalPersonalDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalPersonalDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = SalPersonalDetails
        exclude = ('additional_details_id', 'per_det_id',)
        widgets = {
            'dob': widgets.DateInput(attrs={'type': 'date'})
        }
    

class SalCompanyDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalCompanyDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = SalCompanyDetails
        exclude = ('comp_det_id', 'addi_details_id',)


class SalResidenceDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalResidenceDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = SalResidenceDetails
        exclude = ('sal_res_det_id', 'addi_details_id',)


class SalExistingLoanDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalExistingLoanDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = SalExistingLoanDetails
        exclude = ('existing_loan_det_id', 'addi_details_id',)
        widgets = {
            'emi_start_date': widgets.DateInput(attrs={'type': 'date'}),
            'emi_end_date': widgets.DateInput(attrs={'type': 'date'}),
        }
    

class SalExistingCreditCardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalExistingCreditCardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = SalExistingCreditCard
        exclude = ('existing_credit_card_id', 'addi_details_id',)


class SalAdditionalDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalAdditionalDetailsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = SalAdditionalDetails
        exclude = ('sal_add_det_id', 'addi_details_id',)
        widgets = {
            'loan_inquiry_disbursement_details': forms.Textarea(attrs={'rows':2}),
            }
    

class SalInvestmentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalInvestmentsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = SalInvestments
        exclude = ('sal_inv_id', 'addi_details_id',)