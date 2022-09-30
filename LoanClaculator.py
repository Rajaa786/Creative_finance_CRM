from account.models import *
from HomeLoan.models import *
from datetime import date

class AgeVerification:

    @staticmethod
    def minAge(per_det, age):
        if int(per_det.age) < int(age.min_age):
            return True
        return False

    @staticmethod
    def retireAge(per_det, age, cmp_det, bank, add_det):
        retire_age = int(per_det.retire_age)
        if cmp_det.comp_type == "govt":
            retire_age = int(age.max_age_consi_gov)
        else:
            if retire_age < int(age.retire_age) or (retire_age > int(age.retire_age) and int(per_det.proof) == 0):
                retire_age = int(age.retire_age)
            elif retire_age > int(age.retire_age) and int(per_det.proof) == 1:
                if retire_age > int(age.max_age_consi_others):
                    retire_age = int(age.max_age_consi_others)
        remark = f"Your retirement age is considered as {retire_age}"
        return retire_age, remark


class PropertyVerification:

    def __init__(self, id, bank):
        self.rooms = []
        self.stages = []
        self.neg_areas = []
        self.prop_det = PropertyDetails.objects.filter(lead_id = id).first()
        if self.prop_det.prop_type == "Underconstruction and Buying From Builder" or self.prop_det.prop_type == "Underconstruction and Buying From Seller" or self.prop_det.prop_type == "Ready Possession and Buying From Builder":
            self.p_type = 1
            self.property_type = PropType1.objects.filter(prop_det_id = self.prop_det.prop_det_id).first()
        elif self.prop_det.prop_type == "Resale and Buying From Seller":
            self.p_type = 2 
            self.property_type = PropType2.objects.filter(prop_det_id = self.prop_det.prop_det_id).first()
        else:
            self.p_type = 3
            self.property_type = PropType3.objects.filter(prop_det_id = self.prop_det.prop_det_id).first()
        self.prop = Property.objects.filter(bank_id = bank.bank_id).first()
        self.prop_type = PropertyType.objects.filter(bank_id = bank.bank_id)
        self.stage_of_cons = StageOfConstruction.objects.filter(bank_id = bank.bank_id)
        self.room_type = RoomType.objects.filter(bank_id = bank.bank_id)
        self.negative_area = NegativeArea.objects.filter(bank_id = bank.bank_id)

    def roomConsiderByBank(self):
        for room in self.room_type:
            self.rooms.append(room.room_type.strip())
        if self.property_type.room_type.strip() not in self.rooms:
            return False
        return True

    def stageConsiderByBank(self):
        for stage in self.stage_of_cons:
            self.stages.append(stage.stage.strip())
        if self.property_type.const_stage.strip() not in self.stages:
            return False
        return True

    def completionConsiderByBank(self):
        if int(self.property_type.per_complete) < int(self.prop.perc_completion):
            return False
        return True

    def negativeAreaConsiderByBank(self):
        for negareas in self.negative_area:
            self.neg_areas.append(negareas.neg_area.strip())
        if self.property_type.prop_loc.strip() in self.neg_areas:
            return False
        return True

class LoanCalculation:
    
    @staticmethod
    def calcTenure(retire_age, age, oth_tenure):
        tenure = (retire_age - int(age))*12
        if int(oth_tenure)*12 < tenure:
                tenure = int(oth_tenure)*12
        return tenure

    @staticmethod
    def calcBonus(inc_bonus, bonusType, bonus_amt, bonus_avg_yearly_percent, bonus_avg_half_yearly_percent, bonus_avg_qtr_percent, bonus_avg_monthly_percent):
        bonus = 0
        if inc_bonus == "Y":
            if bonusType == "Yearly":
                per = int(bonus_avg_yearly_percent)
                bonus = (int(bonus_amt)/36)*(per/100)
            elif bonusType == "Half Yearly":
                per = int(bonus_avg_half_yearly_percent)
                bonus = (int(bonus_amt)/12)*(per/100)
            elif bonusType == "Quarterly":
                per = int(bonus_avg_qtr_percent)
                bonus = (int(bonus_amt)/12)*(per/100)
            elif bonusType == "Monthly":
                per = int(bonus_avg_monthly_percent)
                bonus = (int(bonus_amt)/6)*(per/100)
        return bonus

    @staticmethod
    def calcIncentives(inc_incentive, incentivesType, incentive_amt, bonus_avg_yearly_percent, bonus_avg_half_yearly_percent, bonus_avg_qtr_percent, incen_percent):
        incentives = 0
        if inc_incentive == "Y":
            if incentivesType == "Yearly":
                per = int(bonus_avg_yearly_percent)
                incentives = (int(incentive_amt)/36)*(per/100)
            elif incentivesType == "Half Yearly":
                per = int(bonus_avg_half_yearly_percent)
                incentives = (int(incentive_amt)/12)*(per/100)
            elif incentivesType == "Quarterly":
                per = int(bonus_avg_qtr_percent)
                incentives = (int(incentive_amt)/12)*(per/100)
            elif incentivesType == "Monthly":
                per = int(incen_percent)
                incentives = (int(incentive_amt)/6)*(per/100)
        return incentives

    @staticmethod
    def clacRentalIncome(inc_rent_income, rent_agreement_type, oth_inc, rent_ref_in_bank, rent_inc_percent):
        rental_income = 0
        if inc_rent_income == "Y":
            agreement_type = []
            s = rent_agreement_type
            if s.find("/") != -1:
                agreement_type = s.split("/")
            else:
                agreement_type.append(s)

            for i in range(len(agreement_type)):
                agreement_type[i] = agreement_type[i].strip()
            
            for other_inc in oth_inc:
                if int(other_inc.reflection_in_bank_acc) >= int(rent_ref_in_bank):
                    if other_inc.agreement_Type in agreement_type:
                        rental_income += (int(other_inc.rent_amount)*(int(rent_inc_percent)/100))
        return rental_income

    @staticmethod
    def calcIncomeFOIR(income, inc_foir):
        for e in inc_foir:
            if income >= int(e.min_amt):
                if int(e.max_amt) == -1 or income <= int(e.max_amt):
                    foir_percent = int(e.percent)
                    income_foir = income*(int(e.percent)/100)
                    break
        return foir_percent, income_foir

    @staticmethod
    def calcObligation(emi_oblig, credit_card_oblig, exi_loan, exi_card, emi_oblig_not_consi, credit_card_oblig_percent):
        obligation = 0
        if emi_oblig == "Y":
            for loan in exi_loan:
                emi_months = 0
                end_date = loan.emi_end_date
                today = date.today()
                year = end_date.year - today.year
                emi_months += year*12
                if end_date.month > today.month:
                    emi_months += end_date.month - today.month
                else:
                    emi_months -= today.month - end_date.month
                
                if emi_months > int(emi_oblig_not_consi):
                    obligation += int(loan.emi)
        
        # --> ADD KARNA HAI
        if credit_card_oblig == "Y":
            for card in exi_card:
                if card.limit_utilized != "":
                    obligation += (int(card.limit_utilized)*(credit_card_oblig_percent/100))
        return obligation

    @staticmethod
    def calcROI(prevailing_rate, cibil_score, oth_roi, gender, amt, cibil_type):
        roi = float(prevailing_rate)
        cibil = int(cibil_score)
        flag = True
        if cibil_type == "Not Known":
            return roi
        else:
            # Flag variable on line 186 should be here and on line 180 should be deleted once cibil chart of every bank is entered
            for e in oth_roi:
                flag = False
                if amt >= int(e.min_loan_amt) and (int(e.max_loan_amt) == -1 or amt < int(e.max_loan_amt) ):
                    if cibil >= int(e.min_val):
                        if int(e.max_val) == -1 or cibil <= int(e.max_val):
                            if gender == "Female":
                                roi = float(e.roi_women)
                            else:
                                roi = float(e.roi_men)
                            flag = True
                            break
        if not flag:
            return -1
        return roi

    @staticmethod
    def calcPerLacEMI(roi, tenure):
        roi = roi/1200    
        emi = (100000*roi*(1+roi)**tenure)/((1+roi)**tenure-1)
        return emi

    @staticmethod
    def calcUnderconstructionLTV(agreement_val, ltv):
        rbi = 0
        ammenity = 0
        ttl_eli = 0
        ttl_per = 0
        for e in ltv:
            if agreement_val >= int(e.min_amount):
                if int(e.max_amount) == -1 or agreement_val <= int(e.max_amount):
                    rbi = int(e.rbi_guidelines)
                    ammenity = int(e.ammenity)
             
                    break
        ttl_per = rbi + ammenity
        ttl_eli = (agreement_val*ttl_per)/100
        return ttl_eli

    @staticmethod
    def calcResaleLTV(market_val, agreement_val, stp_amt, reg_amt, ltv):
        amount = agreement_val + stp_amt + reg_amt
        for e in ltv:
            if amount >= int(e.min_amount):
                if int(e.max_amount) == -1 or amount <= int(e.max_amount):
                    total = e.total
                    market_value = e.market_value
                    av_capping = e.av_capping
                    amt1 = amount*(total/100)
                    amt2 = market_val*(market_value/100)
                    amt3 = agreement_val*(av_capping/100)
                    if amt1 < amt2 and amt1 < amt3:
                        return amt1
                    elif amt2 < amt3:
                        return amt2
                    else:
                        return amt3