from django.db import models
from django.conf import settings
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Prefix(models.Model): 
    prefix           = models.CharField(max_length=5)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.prefix

class Gender(models.Model): 
    gender           = models.CharField(max_length=10)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.gender

class Relation(models.Model): 
    name             = models.CharField(max_length=20)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.name


class MaritalStatus(models.Model): 
    marital_status   = models.CharField(max_length=10)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.marital_status

class Qualification(models.Model): 
    qualification    = models.CharField(max_length=25)
    is_degree        = models.BooleanField(default=False)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.qualification

class Profession(models.Model): 
    profession       = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.profession

class Role(models.Model): 
    role             = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)

class Product(models.Model): 
    product          = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.product

class SubProduct(models.Model): 
    sub_product      = models.CharField(max_length=50)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    product          = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self): 
        return self.sub_product

class CustomerType(models.Model): 
    cust_type        = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.cust_type
class DesignationType(models.Model): 
    desg_type        = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.desg_type
class CompanyType(models.Model): 
    company_type     = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.company_type
class SalaryType(models.Model): 
    salary_type      = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.salary_type
class ResidenceType(models.Model): 
    residence_type   = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.residence_type
class BankName(models.Model): 
    bank_name        = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.bank_name
class LeadSource(models.Model): 
    lead_source      = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.lead_source

class Degree(models.Model): 
    degree           = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.degree

class LawyerType(models.Model): 
    lawyer_type      = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.lawyer_type

class Nationality(models.Model): 
    nationality      = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.nationality

class Country(models.Model): 
    country          = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.country

class CibilType(models.Model): 
    cibil_type       = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.cibil_type

class State(models.Model): 
    state            = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.state

class City(models.Model): 
    city_name        = models.CharField(max_length=25, default='')
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    state            = models.ForeignKey(State, on_delete=models.CASCADE)
    def __str__(self): 
        return self.city_name
class ApplicantType(models.Model): 
    applicant_type   = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.applicant_type

class PropertyIn(models.Model): 
    property_in      = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.property_in

class Status(models.Model): 
    status           = models.CharField(max_length=55)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.status

class NatureOfBusiness(models.Model): 
    nature_business  = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.nature_business

class AYYear(models.Model): 
    ay_year          = models.CharField(max_length=7)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.ay_year

class AgreementType(models.Model): 
    agreement_type   = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.agreement_type

class StageOfConstruction(models.Model): 
    stage            = models.CharField(max_length=25)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.stage

class RejectionType(models.Model): 
    rejection_type   = models.CharField(max_length=45)
    rejection_reason = models.CharField(max_length=60)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)

# Create your models here.
class AreaIn(models.Model): 
    area_in          = models.CharField(max_length=50)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.area_in

class AreaType(models.Model): 
    area_type        = models.CharField(max_length=50)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.area_type

class RoomType(models.Model): 
    room_type        = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.room_type

class DefaultYear(models.Model): 
    default_year     = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.default_year

class BonusType(models.Model): 
    bonus_type       = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.bonus_type

class IncentivesType(models.Model): 
    incentives_type  = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.incentives_type

class DeductionType(models.Model): 
    deduction_type   = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.deduction_type


class LesseType(models.Model): 
    lesse_type       = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.lesse_type

class PaymentDelayYear(models.Model): 
    payment_delay_year = models.CharField(max_length=30)
    effective_date     = models.DateField(null = True)
    ineffective_date   = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.payment_delay_year


class CompanyName(models.Model): 
    company_name     = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.company_name


class EmploymentType(models.Model): 
    employment_type  = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.employment_type


class InvestmentType(models.Model): 
    investment_type  = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.investment_type


class ProductsOrServices(models.Model): 
    products_or_services = models.CharField(max_length=30)
    effective_date       = models.DateField(null = True)
    ineffective_date     = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.products_or_services


class CibilLoanType(models.Model): 
    cibil_loan_type  = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.cibil_loan_type


class PropertyType(models.Model): 
    property_type    = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.property_type


class NegativeArea(models.Model): 
    negative_area    = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.negative_area

class LoanAmount(models.Model): 
    loan_amount      = models.CharField(max_length=30)
    min_loan_amount  = models.IntegerField()
    max_loan_amount  = models.IntegerField()
    total_exp        = models.IntegerField()
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.loan_amount


class RateOfInterest(models.Model): 
    rate_of_interest = models.CharField(max_length=30)
    effective_date   = models.DateField(null = True)
    ineffective_date = models.DateField(blank=True, null = True)
    def __str__(self): 
        return self.rate_of_interest