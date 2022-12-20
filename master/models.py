from email.utils import formatdate
from hashlib import blake2b
from tokenize import blank_re
from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

YES_NO_CHOICES = ((None, ("Select Yes Or No")), (True, ("Yes")), (False, ("No")))


class Prefix(models.Model):
    prefix = models.CharField(max_length=5)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.prefix


class Gender(models.Model):
    gender = models.CharField(max_length=10)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.gender


class Relation(models.Model):
    name = models.CharField(max_length=20)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class MaritalStatus(models.Model):
    marital_status = models.CharField(max_length=10)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.marital_status


class Qualification(models.Model):
    qualification = models.CharField(max_length=25)
    degree = models.BooleanField(default=False)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.qualification


class Commission(models.Model):
    Commissiontype = models.CharField(max_length=100)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.Commissiontype


class Comissionrates(models.Model):
    Commissionrate = models.IntegerField(null=True)
    Commissiontype = models.ForeignKey(Commission, on_delete=models.CASCADE)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.Commissionrate


class Profession(models.Model):
    profession = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.profession


class Role(models.Model):
    role = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)


class Product(models.Model):
    product = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.product


class SubProduct(models.Model):
    sub_product = models.CharField(max_length=50)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_product


class CustomerType(models.Model):
    cust_type = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.cust_type


class DesignationType(models.Model):
    desg_type = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.desg_type


class CompanyType(models.Model):
    company_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.company_type


class BankName(models.Model):
    bank_name = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.bank_name


class LeadSource(models.Model):
    lead_source = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.lead_source


class Degree(models.Model):
    degree = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.degree


class LawyerType(models.Model):
    lawyer_type = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.lawyer_type


class Nationality(models.Model):
    nationality = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nationality


class Country(models.Model):
    country = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.country


class CibilType(models.Model):
    cibil_type = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.cibil_type


class State(models.Model):
    state = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.state


class City(models.Model):
    city_name = models.CharField(max_length=25, default="")
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name


class ApplicantType(models.Model):
    applicant_type = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.applicant_type


class PropertyIn(models.Model):
    property_in = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.property_in


class Status(models.Model):
    status = models.CharField(max_length=55)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.status


class NatureOfBusiness(models.Model):
    nature_business = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nature_business


class AYYear(models.Model):
    ay_year = models.CharField(max_length=7)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.ay_year


class AgreementType(models.Model):
    agreement_type = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.agreement_type


class StageOfConstruction(models.Model):
    stage = models.CharField(max_length=25)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.stage


class RejectionType(models.Model):
    rejection_type = models.CharField(max_length=45)
    rejection_reason = models.CharField(max_length=60)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)


# Create your models here.


class AreaIn(models.Model):
    area_in = models.CharField(max_length=50)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.area_in


class AreaType(models.Model):
    area_type = models.CharField(max_length=50)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.area_type


class RoomType(models.Model):
    room_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.room_type


class DefaultYear(models.Model):
    default_year = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.default_year


class BonusType(models.Model):
    bonus_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.bonus_type


class IncentivesType(models.Model):
    incentives_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.incentives_type


# class DeductionType(models.Model):
#     deduction_type = models.CharField(max_length=30)
#     effective_date = models.DateField(null=True)
#     ineffective_date = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return self.deduction_type


class LesseType(models.Model):
    lesse_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.lesse_type


class PaymentDelayYear(models.Model):
    payment_delay_year = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.payment_delay_year


class CompanyName(models.Model):
    company_name = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.company_name


class EmploymentType(models.Model):
    employment_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.employment_type


class InvestmentType(models.Model):
    investment_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.investment_type


class ProductsOrServices(models.Model):
    products_or_services = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.products_or_services


class CompanyCatergoryTypes(models.Model):
    cocat_type = models.CharField(max_length=50)
    banks = models.ManyToManyField(BankName)

    def __str__(self):
        return self.cocat_type


class FoirCategory(models.Model):
    cocat_type = models.CharField(max_length=200)
    cutoff = models.IntegerField()
    roi = models.FloatField()
    min_loan_amt = models.BigIntegerField()
    max_loan_amt = models.BigIntegerField()


class SalaryType(models.Model):
    salary_type = models.CharField(max_length=25)

    def __str__(self):
        return self.salary_type


class ResidenceType(models.Model):
    residence_type = models.CharField(max_length=25)

    def __str__(self):
        return self.residence_type


class Cibil(models.Model):
    cibil_score = models.IntegerField()


class Tenure(models.Model):
    ten_type = models.IntegerField()

    def __str__(self):
        return str(self.ten_type)


class BankCategory(models.Model):
    bank_name = models.ForeignKey(BankName, on_delete=models.CASCADE, blank=False)
    company_name = models.ForeignKey(CompanyName, on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(
        CompanyCatergoryTypes, on_delete=models.CASCADE, blank=False
    )
    effective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.bank_name.bank_name + "_" + self.company_name.company_name + "_" + self.category.cocat_type)


class MultiplierCategory(models.Model):
    cocat_type = models.CharField(max_length=200)
    multiplier_number = models.IntegerField()
    roi = models.FloatField()
    min_loan_amt = models.BigIntegerField()
    max_loan_amt = models.BigIntegerField()


class PerTenure_Multiplier_Data(models.Model):
    associated_tenure = models.ForeignKey(Tenure , on_delete=models.CASCADE)
    multiplier = models.IntegerField()


class PerTenure_Foir_Data(models.Model):
    associated_tenure = models.ForeignKey(Tenure , on_delete=models.CASCADE)
    foir = models.IntegerField()

class Multiplier_Data(models.Model):
    min_salary = models.BigIntegerField()
    max_salary = models.BigIntegerField()
    tenure_multipliers = models.ManyToManyField(PerTenure_Multiplier_Data)



class Multiplier_Info(models.Model):
    cocat_type = models.CharField(max_length=250)
    multiplier_data = models.ManyToManyField(Multiplier_Data)


class Foir_Data(models.Model):
    min_salary = models.BigIntegerField()
    max_salary = models.BigIntegerField()
    tenure_foirs = models.ManyToManyField(PerTenure_Foir_Data)

class Foir_Info(models.Model):
    cocat_type = models.CharField(max_length=250)
    foir_data = models.ManyToManyField(Foir_Data)

class AdditionalRate_Info(models.Model):
    min_salary = models.BigIntegerField(null=True)    
    max_salary = models.BigIntegerField(null=True)
    loan_min_amount = models.BigIntegerField()
    loan_max_amount = models.BigIntegerField()
    rate_of_interest = models.BigIntegerField()


class RateOfInterest_Info(models.Model):
    cocat_type = models.CharField(max_length=250 , null=True)
    additional_rate_info = models.ManyToManyField(AdditionalRate_Info)



class Product_and_Policy_Master(models.Model):
    customer_type = models.ForeignKey(
        CustomerType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="cust_types",
    )
    product_name = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    bank_names = models.ForeignKey(
        BankName, on_delete=models.CASCADE, null=False, blank=False
    )
    is_salary_account = models.BooleanField(null=False, choices=YES_NO_CHOICES)
    designation = models.ForeignKey(
        DesignationType, on_delete=models.CASCADE, null=False, blank=False
    )
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    internal_customer = models.BigIntegerField()
    external_customer = models.BigIntegerField()
    current_experience = models.IntegerField()
    total_experience = models.IntegerField()
    cibil_score = models.BigIntegerField(null=False, blank=False)
    processing_fee = models.BigIntegerField()
    months_for_foir = models.BigIntegerField()
    effective_date = models.DateField(blank=True, null=True)
    ineffective_date = models.DateField(null=True, blank=True)
    gross_min = models.BigIntegerField()
    gross_max = models.BigIntegerField()
    net_min = models.BigIntegerField()
    net_max = models.BigIntegerField()
    multiple_enquiry = models.IntegerField()
    emi_bounces = models.IntegerField()
    credit_card_dpd = models.IntegerField()
    credit_card_obligation = models.IntegerField()
    emi_obligation = models.IntegerField()

    multiplier_info = models.ManyToManyField(Multiplier_Info)
    foir_info = models.ManyToManyField(Foir_Info)
    salary_type = models.ManyToManyField(
        SalaryType)
    residence_type = models.ManyToManyField(
        ResidenceType)
    company_type = models.ManyToManyField(CompanyType)
    rate_of_interest = models.ManyToManyField(RateOfInterest_Info)

    def __str__(self):
        s = (
            self.bank_names.bank_name[:4]
            + self.product_name.product[:3]
            + self.customer_type.cust_type[:3]
        )
        return s.upper()


class CibilLoanType(models.Model):
    cibil_loan_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.cibil_loan_type


class PropertyType(models.Model):
    property_type = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.property_type


class NegativeArea(models.Model):
    negative_area = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.negative_area


class LoanAmount(models.Model):
    loan_amount = models.CharField(max_length=30)
    min_loan_amount = models.IntegerField()
    max_loan_amount = models.IntegerField()
    total_exp = models.IntegerField()
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.loan_amount


class RateOfInterest(models.Model):
    rate_of_interest = models.CharField(max_length=30)
    effective_date = models.DateField(null=True)
    ineffective_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.rate_of_interest
