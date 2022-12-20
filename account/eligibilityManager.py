from master.models import BankCategory
from .registerManager import get_tenure_months

TENURE_AVAILABLE = None

def get_Available_Tenure(age , retirement_age):
    global TENURE_AVAILABLE
    if TENURE_AVAILABLE:
         return TENURE_AVAILABLE
    TENURE_AVAILABLE = get_tenure_months(age , retirement_age)
    return TENURE_AVAILABLE



def check_cibil_score(customer_cibil_score, product_cibil_score):
    return customer_cibil_score > product_cibil_score


def check_tenure_availability(age,  retirement_age, tenure_asked, current_tenure):
    tenure_available = get_Available_Tenure(age , retirement_age)

    if tenure_available >= current_tenure.ten_type:
        return True
    else: 
        return False


def check_salary_type(cust_salary_type):
    return cust_salary_type in ['Bank Transfer']


def check_gross_salary(cust_gross, product_gross_min, product_gross_max):
    return cust_gross >= product_gross_min and cust_gross <= product_gross_max


def check_net_salary(cust_net, product_net_min, product_net_max):
    return cust_net >= product_net_min and cust_net <= product_net_max


def check_company_type(cust_company_type):
    return cust_company_type in ['Proprietorship']


def check_designation_type(cust_designation_type):
    return cust_designation_type in ['Below Officer Level']


def check_current_and_total_experience(cust_current_exp, cust_total_exp, product_current_exp, product_total_exp):

    current_exp = cust_current_exp >= product_current_exp,
    total_exp = cust_total_exp >= product_total_exp
    experience_info = {
        'eligibile': True ,
        'non_eligibility_reasons' : []
    }

    if not current_exp:
        experience_info['eligibile'] = False
        experience_info['non_eligibility_reasons'].append(
            f"Current experience must be greater than {product_current_exp}")

    if not total_exp:
        experience_info['eligibile'] = False
        experience_info['non_eligibility_reasons'].append(
            f"Total experience must be greater than {product_total_exp}")

    return experience_info


def check_employment_type(cust_employment_type):
    return cust_employment_type in ['Permanent']



def check_residence_type(residence_details):
    return residence_details.current_residence_type.residence_type in ['Chawl' , "Slum"]




def get_related_bank_categories(product_bank_name , cust_company_name):
    return BankCategory.objects.filter( bank_name = product_bank_name , company_name = cust_company_name).first()