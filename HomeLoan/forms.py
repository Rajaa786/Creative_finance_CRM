from django.forms import DateField, widgets
from django import forms
from django.forms.models import *
from django.forms.widgets import EmailInput, NumberInput, TextInput
from .models import *
from account.models import *
from django.db.models import Q
from datetime import *
from master.models import *
from django.db.models import Q


class ProductsandPolicyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductsandPolicyForm, self).__init__(*args, **kwargs)
        self.fields['prod_name'] = ModelChoiceField(queryset=Product.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None)), empty_label="-- Select Product --")
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        if 'prod_name' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['sub_product'].queryset = SubProduct.objects.filter(
                    product=product_id)
            except(ValueError, TypeError):
                pass

    class Meta:
        model = ProductsAndPolicy
        exclude = ('pid', 'lock', 'effective_date')
        widgets = {
            'effective_date': widgets.DateInput(attrs={'type': 'date'}),
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'productandpolicy_name': "Product And Policy Code Name",
            'prod_name': "Product Name",
            'sub_product': "Sub-Product",
        }


class HlBasicDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HlBasicDetailsForm, self).__init__(*args, **kwargs)
        self.fields['form_16'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                            (True, 'Yes'),
                                                            (False, 'No')),
                                                   )
        self.fields['company_profitability'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                          (True,
                                                                           'Yes'),
                                                                          (False, 'No')),
                                                                 )
        self.fields['negative_employer_profile'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                              (True,
                                                                               'Yes'),
                                                                              (False, 'No')),
                                                                     )
        self.fields['profession_tax_deduction'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                             (True,
                                                                              'Yes'),
                                                                             (False, 'No')),
                                                                    )
        self.fields['customer_type'] = ModelChoiceField(queryset=CustomerType.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None)), empty_label="-- Select Customer --")
        self.fields['designation'] = ModelMultipleChoiceField(queryset=DesignationType.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None)))
        self.fields['company_type'] = ModelMultipleChoiceField(queryset=CompanyType.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None)))
        self.fields['salary_type'] = ModelChoiceField(queryset=SalaryType.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None)), empty_label="-- Select SalaryType --")
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = HlBasicDetails
        exclude = ('pid', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'}),
        }


class HlObligationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HlObligationForm, self).__init__(*args, **kwargs)
        self.fields['credit_card'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                (True, 'Yes'),
                                                                (False, 'No')),
                                                       )
        self.fields['emi_obligation'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                   (True, 'Yes'),
                                                                   (False, 'No')),
                                                          )
        self.fields['gold_loan'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                              (True, 'Yes'),
                                                              (False, 'No')),
                                                     )
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = HlObligation
        exclude = ('pid', 'basic_details_id', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'})
        }


class HlOtherDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HlOtherDetailsForm, self).__init__(*args, **kwargs)
        self.fields['inward_cheque_return'] = forms.ChoiceField(
            choices=((None, '--Yes Or No --'), (True, 'Yes'), (False, 'No')))
        self.fields['multiple_inquiry'] = forms.ChoiceField(
            choices=((None, '--Yes Or No --'), (True, 'Yes'), (False, 'No')))
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = HlOtherDetails
        exclude = ('pid', 'basic_details_id', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'})
        }


class HlPropertyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HlPropertyForm, self).__init__(*args, **kwargs)
        self.fields['property_type'].queryset = PropertyType.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None))
        self.fields['stage_of_construction'].queryset = StageOfConstruction.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None))
        self.fields['builder_category'] = forms.ChoiceField(
            choices=((None, '--Yes Or No--'), (True, 'Yes'), (False, 'No')))
        self.fields['occupation_certificate'] = forms.ChoiceField(
            choices=((None, '--Yes Or No--'), (True, 'Yes'), (False, 'No')))
        self.fields['cc_municipal_plan_tax_receipt'] = forms.ChoiceField(
            choices=((None, '--Yes Or No--'), (True, 'Yes'), (False, 'No')))
        self.fields['subvention_scheme'] = forms.ChoiceField(
            choices=((None, '--Yes Or No--'), (True, 'Yes'), (False, 'No')))
        self.fields['previous_aggrement_available'] = forms.ChoiceField(
            choices=((None, '--Yes Or No--'), (True, 'Yes'), (False, 'No')))
        self.fields['apf'] = forms.ChoiceField(
            choices=((None, '--Yes Or No--'), (True, 'Yes'), (False, 'No')))
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = HlProperty
        exclude = ('pid', 'basic_details_id', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'})
        }


class HlLoan_To_Value_Type_1Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HlLoan_To_Value_Type_1Form, self).__init__(*args, **kwargs)
        self.fields['loan_amount'] = ModelChoiceField(queryset=LoanAmount.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None)))
        self.fields['car_parking'] = forms.ChoiceField(
            choices=((None, '--Yes Or No--'), (True, 'Yes'), (False, 'No')))
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['loan_amount'].queryset = LoanAmount.objects.filter(
            Q(ineffective_date__gte=datetime.now()) | Q(ineffective_date=None))

    class Meta:
        model = HlLoan_To_Value_Type_1
        exclude = ('pid', 'basic_details_id', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'})
        }


class HlLoan_To_Value_Type_2Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HlLoan_To_Value_Type_2Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = HlLoan_To_Value_Type_2
        exclude = ('pid', 'basic_details_id', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'})
        }


class HlIncomeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HlIncomeForm, self).__init__(*args, **kwargs)
        self.fields['gross_salary'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                 (True, 'Yes'),
                                                                 (False, 'No')),
                                                        )
        self.fields['net_salary'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                               (True, 'Yes'),
                                                               (False, 'No')),
                                                      )
        self.fields['bonus'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                          (True, 'Yes'),
                                                          (False, 'No')),
                                                 )
        self.fields['income_foir_monthly'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                        (True,
                                                                         'Yes'),
                                                                        (False, 'No')),
                                                               )
        self.fields['income_foir_yearly'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                       (True,
                                                                        'Yes'),
                                                                       (False, 'No')),
                                                              )
        self.fields['income_foir_quarterly'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                          (True,
                                                                           'Yes'),
                                                                          (False, 'No')),
                                                                 )
        self.fields['income_foir_half_yearly'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                            (True,
                                                                             'Yes'),
                                                                            (False, 'No')),
                                                                   )
        self.fields['rent_income'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                (True, 'Yes'),
                                                                (False, 'No')),
                                                       )
        self.fields['bank_reflection'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                    (True, 'Yes'),
                                                                    (False, 'No')),
                                                           )
        self.fields['co_applicant_no_income_only_rent_income'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                                            (True,
                                                                                             'Yes'),
                                                                                            (False, 'No')),
                                                                                   )
        self.fields['co_applicant_mandatory'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                           (True,
                                                                            'Yes'),
                                                                           (False, 'No')),
                                                                  )
        self.fields['incentive'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                              (True, 'Yes'),
                                                              (False, 'No')),
                                                     )
        self.fields['income_foir_incentive'] = forms.ChoiceField(choices=((None, '-- Yes Or No --'),
                                                                          (True,
                                                                           'Yes'),
                                                                          (False, 'No')),
                                                                 )
        self.fields['future_rent'] = forms.ChoiceField(choices=(
            (None, '-- Yes Or No --'),
            (True, 'Yes'),
            (False, 'No'),
        )
        )
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = HlIncome
        exclude = ('pid', 'basic_details_id', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'}),
        }


class HlIncomeFoirForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(HlIncomeFoirForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = HlIncomeFoir
        exclude = ('pid', 'basic_details_id', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'}),
        }


class CibilForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CibilForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Cibil
        exclude = ('pid', 'basic_details_id', 'cibil_id', 'effective_date')
        widgets = {
            'ineffective_date': widgets.DateInput(attrs={'type': 'date'}),
        }
