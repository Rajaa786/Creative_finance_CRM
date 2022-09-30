from account.models import *
from HomeLoan.models import *
from master.models import *

class Eligibility_Underconstruction:
    def __init__(self, pap, applicant):
        SalIncomeDetailsData           = SalIncomeDetails.objects.get(addi_details_id = applicant.pk)
        SalPersonalDetailsData         = SalPersonalDetails.objects.get(additional_details_id = applicant.pk)
        self.app_present_age           = SalPersonalDetailsData.age
        self.app_company_type          = SalCompanyDetails.objects.get(addi_details_id = applicant.pk).company_type
        self.app_retirement_age        = SalPersonalDetailsData.retirement_age
        self.app_net_monthly_salary    = SalIncomeDetailsData.net_sal
        self.app_gross_monthly_salary  = SalIncomeDetailsData.gross_sal
        self.app_monthly_incentive     = SalIncomeDetailsData.incentive_amount / SalIncomeDetailsData.incentive_duration if ((SalIncomeDetailsData.incentive_duration > 0) and (SalIncomeDetailsData.incentive_amount > 0)) else 0
        self.app_monthly_bonus         = SalIncomeDetailsData.bonus_amount / SalIncomeDetailsData.bonus_duration if ((SalIncomeDetailsData.bonus_duration > 0) and (SalIncomeDetailsData.bonus_amount > 0)) else 0
        self.app_monthly_rental_income = SalOtherIncomes.objects.get(addi_details_id = applicant.pk).rental_income
        self.app_rate_of_interest      = RateOfInterest.objects.latest('pk').rate_of_interest
        self.app_agreeement_value      = 0
        self.app_market_value          = 0
        if applicant.lead_id.sub_product.sub_product == 'Underconstruction Buying From Builder':
            self.agreement_value = PropType1.objects.get(lead_id = applicant.lead_id).agreement_val
            self.market_value = PropType1.objects.get(lead_id = applicant.lead_id).market_val
        elif applicant.lead_id.sub_product.sub_product == 'Underconstruction Buying From Seller':
            self.agreement_value = PropType2.objects.get(lead_id = applicant.lead_id).agreement_val
            self.market_value = PropType2.objects.get(lead_id = applicant.lead_id).market_val
        elif applicant.lead_id.sub_product.sub_product == 'Ready Possession Buying From Builder':
            self.agreement_value = PropType3.objects.get(lead_id = applicant.lead_id).agreement_val
            self.market_value = PropType3.objects.get(lead_id = applicant.lead_id).market_val
        elif applicant.lead_id.sub_product.sub_product == 'Ready Possession Buying From Seller':
            self.agreement_value = PropType4.objects.get(lead_id = applicant.lead_id).agreement_val
            self.market_value = PropType4.objects.get(lead_id = applicant.lead_id).market_val
        self.loan_requirement = SalPersonalDetails.objects.get(additional_details_id = applicant.pk).loan_amount
        self.AV_to_requirement = (self.loan_requirement / self.agreement_value) * 100
        self.MV_to_requirement = (self.loan_requirement / self.market_value) * 100
    
    def check_income_eligibility(self, pap, applicant):
        SalPersonalDetailsData = SalPersonalDetails.objects.get(additional_details_id = applicant.pk)
        SalOtherIncomesData    = SalOtherIncomes.objects.get(addi_details_id = applicant.pk)
        SalIncomeDetailsData   = SalIncomeDetails.objects.get(addi_details_id = applicant.pk)
        HlBasicDetailsData     = HlBasicDetails.objects.get(pid=pap.pk)
        HlIncomeData           = HlIncome.objects.get(basic_details_id = HlBasicDetailsData.pk)
        HlOtherDetailsData     = HlOtherDetails.objects.get(basic_details_id=HlBasicDetailsData.pk)

        if SalCompanyDetails.objects.get(addi_details_id=applicant.pk).company_type != 'Govt':
            if SalPersonalDetailsData.retirement_age < HlBasicDetailsData.maximum_age_consider_others:
                pap_cons_age_for_others = SalPersonalDetailsData.retirement_age
            else:
                pap_cons_age_for_others = HlBasicDetailsData.maximum_age_consider_others
        else:
            if SalPersonalDetailsData.retirement_age < HlBasicDetailsData.maximum_age_consider_govt:
                pap_cons_age_for_govt = SalPersonalDetailsData.retirement_age
            else:
                pap_cons_age_for_govt = HlBasicDetailsData.maximum_age_consider_govt

        pap_final_age_for_cons = max(pap_cons_age_for_others, pap_cons_age_for_govt)

        if HlIncomeData.incentive == True and SalPersonalDetailsData.incentive_duration > 0 and SalPersonalDetailsData.incentive_amount > 0:
            if self.app_monthly_incentive >= HlIncomeData.min_incentive_avg_monthly and self.app_monthly_incentive <= HlIncomeData.max_incentive_avg_monthly:
                pap_monthly_incentive = self.app_monthly_incentive * HlIncomeData.incentive_avg_monthly_percentage
            else:
                pap_monthly_incentive = 0
            if self.app_monthly_incentive >= HlIncomeData.min_incentive_avg_quarterly and self.app_monthly_incentive <= HlIncomeData.max_incentive_avg_quarterly:
                pap_quarterly_incentive = self.app_monthly_incentive * HlIncomeData.incentive_avg_quarterly_percentage
            else:
                pap_quarterly_incentive = 0
            if self.app_monthly_incentive >= HlIncomeData.min_incentive_avg_half_yearly and self.app_monthly_incentive <= HlIncomeData.max_incentive_avg_half_yearly:
                pap_half_yearly_incentive = self.app_monthly_incentive * HlIncomeData.incentive_avg_half_yearly_percentage
            else:
                pap_half_yearly_incentive = 0
            if self.app_monthly_incentive >= HlIncomeData.min_incentive_avg_yearly and self.app_monthly_incentive <= HlIncomeData.max_incentive_avg_yearly:
                pap_yearly_incentive = self.app_monthly_incentive * HlIncomeData.incentive_avg_yearly_percentage
            else:
                pap_yearly_incentive = 0
        else:
            pap_monthly_incentive     = 0
            pap_quarterly_incentive   = 0
            pap_half_yearly_incentive = 0
            pap_yearly_incentive      = 0

        if HlIncomeData.bonus == True and SalPersonalDetailsData.bonus_duration > 0 and SalPersonalDetailsData.bonus_amount > 0:
            if self.app_monthly_bonus >= HlIncomeData.min_bonus_avg_monthly and self.app_monthly_bonus <= HlIncomeData.max_bonus_avg_monthly:
                pap_monthly_bonus = self.app_monthly_bonus * HlIncomeData.bonus_avg_monthly_percentage
            else:
                pap_monthly_bonus = 0
            if self.app_monthly_bonus >= HlIncomeData.min_bonus_avg_quarterly and self.app_monthly_bonus <= HlIncomeData.max_bonus_avg_quarterly:
                pap_quarterly_bonus = self.app_monthly_bonus * HlIncomeData.bonus_avg_quarterly_percentage
            else:
                pap_quarterly_bonus = 0
            if self.app_monthly_bonus >= HlIncomeData.min_bonus_avg_half_yearly and self.app_monthly_bonus <= HlIncomeData.max_bonus_avg_half_yearly:
                pap_half_yearly_bonus = self.app_monthly_bonus * HlIncomeData.bonus_avg_half_yearly_percentage
            else:
                pap_half_yearly_bonus = 0
            if self.app_monthly_bonus >= HlIncomeData.min_bonus_avg_yearly and self.app_monthly_bonus <= HlIncomeData.max_bonus_avg_yearly:
                pap_yearly_bonus = self.app_monthly_bonus * HlIncomeData.bonus_avg_yearly_percentage
            else:
                pap_yearly_bonus = 0
        else:
            pap_monthly_bonus     = 0
            pap_quarterly_bonus   = 0
            pap_half_yearly_bonus = 0
            pap_yearly_bonus      = 0
        
        if HlIncomeData.rent_income == True and HlIncomeData.rent_agreement_type == SalOtherIncomesData.agreement_type and HlIncomeData.bank_reflection == SalOtherIncomesData.reflection_in_bank_account and SalOtherIncomesData.rent_reflection_in_bank >= HlIncomeData.min_rent_reflection_in_bank and SalOtherIncomesData.rent_reflection_in_bank <= HlIncomeData.max_rent_reflection_in_bank:
            pap_monthly_rental = self.app_monthly_rental_income * HlIncomeData.rent_income_percentage
        else:
            pap_monthly_rental = 0

        pap_all_incentives = pap_monthly_incentive + pap_quarterly_incentive + pap_half_yearly_incentive + pap_yearly_incentive
        pap_all_bonus      = pap_monthly_bonus + pap_quarterly_bonus + pap_half_yearly_bonus + pap_yearly_bonus
        if HlIncomeData.gross_salary == True:
            pap_total_income_for_foir = pap_all_incentives + pap_all_bonus + pap_monthly_rental + SalIncomeDetailsData.gross_sal
            for i in (HlIncomeFoir.objects.filter(basic_details_id=HlBasicDetailsData.pk)):
                if SalIncomeDetailsData.gross_sal >= i.min_income_foir and SalIncomeDetailsData.gross_sal <= i.max_income_foir:
                    pap_iir_or_foir = i.income_foir_percentage
                    break
        elif HlIncomeData.net_salary == True:
            pap_total_income_for_foir = pap_all_incentives + pap_all_bonus + pap_monthly_rental + SalIncomeDetailsData.net_sal
            for i in (HlIncomeFoir.objects.filter(basic_details_id=HlBasicDetailsData.pk)):
                if SalIncomeDetailsData.net_sal >= i.min_income_foir and SalIncomeDetailsData.net_sal <= i.max_income_foir:
                    pap_iir_or_foir = i.income_foir_percentage
                    break
        
        pap_tenure_in_months = (pap_final_age_for_cons - self.app_present_age) * 12

        if pap_tenure_in_months < HlOtherDetailsData.tenure:
            pap_final_tenure_in_months = pap_tenure_in_months
        else:
            pap_final_tenure_in_months = HlOtherDetailsData.tenure
