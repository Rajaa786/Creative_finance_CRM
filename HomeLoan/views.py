from LoanClaculator import AgeVerification, LoanCalculation, PropertyVerification
from django.shortcuts import redirect, render
from datetime import date
from .models import *
from .forms import *
from django.contrib import messages
from account.models import *
from django.contrib.auth.decorators import login_required
from stronghold.decorators import public


# Create your views here.
def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state = state_id)
    return render(request,'HomeLoan/city_dropdown_list_options.html',{'cities':cities})

def load_subproducts(request):
    product_id = request.GET.get('product_id')
    subproducts = SubProduct.objects.filter(product=product_id)
    return render(request,'HomeLoan/subproducts_dropdown_list_options.html',{'subproducts':subproducts})

def eligibility(request, id):
    lead = Leads.objects.filter(pk = id).first()
    add_dets = AdditionalDetails.objects.filter(lead_id = id)     #-> collecting all applicants and co applicants
    banks = Bank.objects.all()
    #-> Dictionaries to collect different data and remarks
    data = {}
    remarks = {}

    for add_det in add_dets:   
        data[add_det.applicant_type] = {}
        remarks[add_det.applicant_type] = {}

        if add_det.cust_type == "Salaried":     #-> calculating for customer type salaried
            banks = Bank.objects.filter(cust_type = "Salaried")

            for bank in banks:
                #-> Setting for each bank
                data[add_det.applicant_type][bank.bank_name] = {}
                remarks[add_det.applicant_type][bank.bank_name] = []

                #-> Checking Property Details which will be only assigned to applicant
                if add_det.applicant_type == "Applicant":
                    prop_det = PropertyDetails.objects.filter(lead_id = id).first()
                    if prop_det.prop_type == "Underconstruction and Buying From Builder" or prop_det.prop_type == "Underconstruction and Buying From Seller" or prop_det.prop_type == "Ready Possession and Buying From Builder":
                        p_type = 1
                        property_type = PropType1.objects.filter(prop_det_id = prop_det.prop_det_id).first()
                    elif prop_det.prop_type == "Resale and Buying From Seller":
                        p_type = 2
                        property_type = PropType2.objects.filter(prop_det_id = prop_det.prop_det_id).first()
                    else:
                        p_type = 3
                        property_type = PropType3.objects.filter(prop_det_id = prop_det.prop_det_id).first()




                    property = PropertyVerification(id, bank)

                    if property.p_type == 3:
                        remarks[add_det.applicant_type][bank.bank_name].append(f"{property.prop_det.prop_type} is not considered by {bank.bank_name}")
                        continue

                    if not property.roomConsiderByBank():
                        remarks[add_det.applicant_type][bank.bank_name].append(f"{bank.bank_name} does not consider {property.property_type.room_type} Room Type")
                        continue

                    if property.p_type == 1:

                        if not property.stageConsiderByBank():
                            remarks[add_det.applicant_type][bank.bank_name].append(f"{bank.bank_name} does not consider {property_type.const_stage} Stage")
                            continue

                        if not property.completionConsiderByBank():
                            remarks[add_det.applicant_type][bank.bank_name].append(f"{bank.bank_name} considers Completion more than {prop.perc_completion}%")
                            continue

                    if property.p_type == 1 or property.p_type == 2:
                        if not property.negativeAreaConsiderByBank():
                            remarks[add_det.applicant_type][bank.bank_name].append(f"{bank.bank_name} does not consider {property_type.prop.loc} Location")
                            continue

                age      = Age.objects.filter(bank_id = bank.bank_id).first()
                oth      = OtherDetails.objects.filter(bank_id = bank.bank_id).first()
                per_det  = SalPersonalDetails.objects.filter(additional_details_id = add_det.pk).first()
                inc      = Income.objects.filter(bank_id = bank.bank_id).first()
                inc_det  = SalIncomeDetails.objects.filter(addi_details_id = add_det.pk).first()
                oth_inc  = SalOtherIncomes.objects.filter(addi_details_id = add_det.pk).first()
                inc_foir = IncomeFoir.objects.filter(bank_id = bank.bank_id).first()
                obl      = Obligation.objects.filter(bank_id = bank.bank_id).first()
                exi_card = SalExistingCreditCard.objects.filter(addi_details_id = add_det.pk).first()
                exi_loan = SalExistingLoanDetails.objects.filter(addi_details_id = add_det.pk).first()
                oth_roi  = OtherDetailsROI.objects.filter(bank_id = bank.bank_id).first()
                cmp_det  = SalCompanyDetails.objects.filter(addi_details_id = add_det.pk).first()


                #-> Checking minimum age
                if AgeVerification.minAge(per_det, age):
                    data[add_det.applicant_type][bank.bank_name] = 0
                    remarks[add_det.applicant_type][bank.bank_name].append(f"Age of applicant should be greater than {age.min_age}")
                    continue

                #-> Checking Nationality
                if per_det.nationality == "Non Resident Indian":
                    remarks[add_det.applicant_type][bank.bank_name].append(f"Nationality Should be Resident")
                    continue

                #-> Retire age
                retire_age, remark = AgeVerification.retireAge(per_det, age, cmp_det, bank, add_det)
                remarks[add_det.applicant_type][bank.bank_name].append(remark)

                #-> Tenure
                tenure = LoanCalculation.calcTenure(retire_age, per_det.age, oth.tenure)
                data[add_det.applicant_type][bank.bank_name]['tenure'] = tenure

                #-> Income calculations

                net_salary = 0
                gross_salary = 0
                incentives = LoanCalculation.calcIncentives(inc.incentive, inc_det.incentivesType, inc_det.incentive_amt, inc.bonus_avg_yearly_percent, inc.bonus_avg_half_yearly_percent, inc.bonus_avg_qtr_percent, inc.incen_percent)
                bonus = LoanCalculation.calcBonus(inc_det.bonusType, inc.bonus, inc_det.bonus_amt, inc.bonus_avg_yearly_percent, inc.bonus_avg_half_yearly_percent, inc.bonus_avg_qtr_percent, inc.incen_percent)
                rental_income = LoanCalculation.clacRentalIncome(inc.rent_income, inc.rent_agreement_type, oth_inc, inc.rent_ref_in_bank, inc.rent_inc_percent)
                total_bns_inc_rent = 0

                if inc.net_sal != "N":
                    net_salary = int(inc_det.net_sal)
                if inc.gross_sal != "N":
                    gross_salary = int(inc_det.gross_sal)

                #-> obligation
                obligation = LoanCalculation.calcObligation(obl.emi_oblig, obl.credit_card, exi_loan, exi_card, obl.emi_oblig_not_consi, obl.credit_card_oblig_percent)
                data[add_det.applicant_type][bank.bank_name]['obligation'] = obligation

                #-> Total extra income
                total_bns_inc_rent = bonus + incentives + rental_income

                #-> Income FOIR
                income = 0
                if gross_salary == 0:
                    income = net_salary
                else:
                    income = gross_salary
                total_income = income + total_bns_inc_rent
                data[add_det.applicant_type][bank.bank_name]['total_income'] = total_income
                foir_percent, income_foir = LoanCalculation.calcIncomeFOIR(total_income, inc_foir)
                data[add_det.applicant_type][bank.bank_name]['foir_per'] = foir_percent
                data[add_det.applicant_type][bank.bank_name]['inc_foir'] = income_foir

                #-> Rate Of Interest
                roi = LoanCalculation.calcROI(oth.prevailing_rate, per_det.cibil_score, oth_roi, per_det.gender, int(per_det.loan_amt), per_det.cibil_type)
                if roi == -1:
                    remarks[add_det.applicant_type][bank.bank_name].append(f"Your CIBIL Score is too low for approval of loan")
                    continue
                data[add_det.applicant_type][bank.bank_name]['roi'] = roi

                #-> Per Lac Emi
                per_lac_emi = LoanCalculation.calcPerLacEMI(roi, tenure)
                data[add_det.applicant_type][bank.bank_name]['per_lac_emi'] = per_lac_emi

                #-> Loan eligibility
                loan_eligibility = (income_foir - obligation)/per_lac_emi
                data[add_det.applicant_type][bank.bank_name]['loan_eligibility'] = loan_eligibility

    #-> Calculating total eligibility of applicants for each bank
    ttl_eli = {}
    p_l_emi = {}
    for bank in banks:
        total_eli = 0
        for key in data.keys():
            if bank.bank_name in data[key].keys():
                if 'loan_eligibility' in data[key][bank.bank_name].keys():
                    total_eli += data[key][bank.bank_name]['loan_eligibility']
                # if 'per_lac_emi' in data[key][bank.bank_name].keys():
                #     p_l_emi[bank.bank_name] = data[key][bank.bank_name]['per_lac_emi']
        ttl_eli[bank.bank_name] = total_eli

    #-> Loan towards valuation
    add_det2 = AdditionalDetails.objects.filter(lead_id = id, applicant_type=1).first()
    app_det = SalPersonalDetails.objects.get(addi_details_id = add_det2.pk)
    agreement_value = int(property.property_type.agreement_val)
    market_value = int(property.property_type.market_val)
    loan_req = int(app_det.loan_amt)
    bank_eli = 0
    loan = 0
    loan_approved = {}


    for bank in banks:
        if loan_req < ttl_eli[bank.bank_name]*100000:
            loan = loan_req
        else:
            loan = ttl_eli[bank.bank_name]*100000

        if p_type == 1:
            ltv = LoanTowardsValuation.objects.filter(bank_id = bank.bank_id)
            bank_eli = LoanCalculation.calcUnderconstructionLTV(agreement_value, ltv)
        if p_type == 2:
            stp_amt = property.property_type.stp_amt
            reg_amt = property.property_type.reg_amt
            ltv = LtvResale.objects.filter(bank_id = bank.bank_id)
            bank_eli = LoanCalculation.calcResaleLTV(market_value, agreement_value, stp_amt, reg_amt, ltv)
        print(bank_eli)
        if bank_eli < loan:
            loan = bank_eli
        loan_approved[bank.bank_name] = round(loan,2)

        for app in data.keys():
            if bank.bank_name in data[app].keys():
                if 'per_lac_emi' in data[key][bank.bank_name].keys():
                    data[app][bank.bank_name]['emi'] = round((loan_approved[bank.bank_name]/100000)*data[app][bank.bank_name]['per_lac_emi'],2)


    display = {}
    for app in data.keys():
        display[app] = {}
        for bank in banks:
            display[app][bank.bank_name] = {}
            if bank.bank_name in data[app].keys():
                if 'tenure' in data[app][bank.bank_name]:
                    display[app][bank.bank_name]['tenure'] = data[app][bank.bank_name]['tenure']
                if 'total_income' in data[app][bank.bank_name]:
                    display[app][bank.bank_name]['total_income'] = round(data[app][bank.bank_name]['total_income'],2)
                if 'loan_eligibility' in data[app][bank.bank_name]:
                    display[app][bank.bank_name]['loan_eligibility'] = round(data[app][bank.bank_name]['loan_eligibility']*100000,2)
                if 'roi' in data[app][bank.bank_name]:
                    display[app][bank.bank_name]['roi'] = data[app][bank.bank_name]['roi']
                if 'per_lac_emi' in data[app][bank.bank_name]:
                    display[app][bank.bank_name]['per_lac_emi'] = round(data[app][bank.bank_name]['per_lac_emi'],2)

    total_emi = {}
    for bank in banks:
        total_emi[bank.bank_name] = 0
        for app in data.keys():
            if 'emi' in data[app][bank.bank_name]:
                total_emi[bank.bank_name] += data[app][bank.bank_name]['emi']
    return render(request, "HomeLoan/eligibility.html", {'remarks':remarks, 'display':display , 'loan_approved':loan_approved, 'total_emi':total_emi})


def PPage(request, ppid):
    if request.method == 'POST':
        min_age = int(request.POST['min_age'])
        retire_age = int(request.POST['retire_age'])
        max_age_consi_others = int(request.POST['max_age_consi_others'])
        max_age_consi_gov = int(request.POST['max_age_consi_gov'])
        bank = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]

        age = Age(min_age=min_age, retire_age=retire_age, max_age_consi_others=max_age_consi_others, max_age_consi_gov=max_age_consi_gov, bank_id=bank)
        age.save()
        return redirect('editproductandpolicy', id=ppid)

    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/age.html', context=context)


def PPeditAge(request, ppid, ageid):
    if request.method == 'POST':
        Age.objects.filter(age_id=ageid).update(
            min_age = int(request.POST['min_age']),
            retire_age = int(request.POST['retire_age']),
            max_age_consi_others = int(request.POST['max_age_consi_others']),
            max_age_consi_gov = int(request.POST['max_age_consi_gov'])
        )
        return redirect('editproductandpolicy', id=ppid)
    context = {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'age': Age.objects.filter(age_id=ageid)[0]
    }
    return render(request, 'HomeLoan/editage.html', context=context)

def PPnegativearea(request, ppid):
    if request.method == 'POST':
        neg_area = request.POST['neg_area']
        bank = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]

        negativearea = NegativeArea(neg_area=neg_area, bank_id=bank)
        negativearea.save()
        return redirect('editproductandpolicy', id=ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/negativearea.html', context=context)

def PPeditNegativearea(request, ppid, negativeareaid):
    if request.method == 'POST':
        NegativeArea.objects.filter(neg_area_id=negativeareaid).update(
            neg_area = request.POST['neg_area']
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'negativearea': NegativeArea.objects.filter(neg_area_id=negativeareaid)[0]
    }
    return render(request, 'HomeLoan/editnegativearea.html', context=context)

def PPbank(request):
    if request.method == 'POST':
        bank_name = request.POST['bank_name']
        cust_type = request.POST['cust_type']
        bank = Bank(bank_name=bank_name, cust_type=cust_type)
        bank.save()
        return redirect('AddProductsAndPolicy')

def PPnegativeemployerprofile(request, ppid):
    if request.method == 'POST':
        neg_emp_pro = request.POST['neg_emp_pro']
        bank = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]

        NegativeEmployerProfile(neg_emp_pro=neg_emp_pro, bank_id=bank).save()
        return redirect('editproductandpolicy', id=ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/negativeemployerprofile.html', context=context)

def PPeditnegativeemployerprofile(request, ppid, negativeemployerprofileid):
    if request.method == 'POST':
        NegativeEmployerProfile.objects.filter(neg_emp_pro_id=negativeemployerprofileid).update(
            neg_emp_pro = request.POST['neg_emp_pro']
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'negativeemployerprofile': NegativeEmployerProfile.objects.filter(neg_emp_pro_id=negativeemployerprofileid)[0]
    }
    return render(request, 'HomeLoan/editnegativeemployerprofile.html', context=context)

def PPCibil(request, ppid):
    if request.method == 'POST':
        cibil_range_min = int(request.POST['cibil_range_min'])
        cibil_range_max = int(request.POST['cibil_range_max'])
        bank = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]

        Cibil(cibil_range_min=cibil_range_min, cibil_range_max=cibil_range_max, bank_id=bank).save()
        return redirect('editproductandpolicy', id=ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/Cibil.html', context=context)

def PPeditCibil(request, ppid, cibilid):
    if request.method == 'POST':
        Cibil.objects.filter(cibil_id=cibilid).update(
            cibil_range_min = request.POST['cibil_range_min'],
            cibil_range_max = request.POST['cibil_range_max']
        )
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'cibil': Cibil.objects.filter(cibil_id=cibilid)[0]
    }
    return render(request, 'HomeLoan/editCibil.html', context=context)


def PPobligation(request, ppid):
    if request.method == 'POST':
        Obligation(
            emi_oblig                 = request.POST['emi_oblig'],
            emi_oblig_not_consi       = request.POST['emi_oblig_not_consi'],
            credit_card               = request.POST['credit_card'],
            credit_card_oblig_percent = int(request.POST['credit_card_oblig_percent']),
            gold_loan                 = request.POST['gold_loan'],
            gold_loan_percent         = int(request.POST['gold_loan_percent']),
            bank_id                   = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/obligation.html', context=context)

def PPeditobligation(request, ppid, obligationid):
    if request.method == 'POST':
        Obligation.objects.filter(obligation_id=obligationid).update(
            emi_oblig                 = request.POST['emi_oblig'],
            emi_oblig_not_consi       = request.POST['emi_oblig_not_consi'],
            credit_card               = request.POST['credit_card'],
            credit_card_oblig_percent = int(request.POST['credit_card_oblig_percent']),
            gold_loan                 = request.POST['gold_loan'],
            gold_loan_percent         = int(request.POST['gold_loan_percent']),
        )
        return redirect('editproductandpolicy', ppid)

    context = {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'pp': ProductsAndPolicy.objects.filter(prod_id=ppid)[0],
        'obligation': Obligation.objects.filter(obligation_id=obligationid)[0],
    }
    return render(request, 'HomeLoan/editobligation.html', context=context)

def PPcompany(request, ppid):
    if request.method == 'POST':
        comp_type = request.POST['comp_type']
        bank = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]

        Company(comp_type=comp_type, bank_id=bank).save()
        return redirect('editproductandpolicy', id=ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/company.html', context=context)

def PPeditcompany(request, ppid, companyid):
    if request.method == 'POST':
        Company.objects.filter(comp_id=companyid).update(
            comp_type = request.POST['comp_type']
        )
        return redirect('editproductandpolicy', ppid)
    context={
        'company': Company.objects.filter(comp_id=companyid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editcompany.html', context=context)

def PPOtherDetailsRoi(request, ppid):
    if request.method == 'POST':
        min_loan_amt = int(request.POST['min_loan_amt'])
        max_loan_amt = int(request.POST['max_loan_amt'])
        min_val = int(request.POST['min_val'])
        max_val = int(request.POST['max_val'])
        roi_men = request.POST['roi_men']
        roi_women = request.POST['roi_women']
        bank = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]

        OtherDetailsROI(
            min_loan_amt=min_loan_amt,
            max_loan_amt=max_loan_amt,
            min_val=min_val,
            max_val=max_val,
            roi_men=roi_men,
            roi_women=roi_women,
            bank_id=bank
        ).save()
        return redirect('editproductandpolicy', id=ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/OtherDetailsRoi.html', context=context)

def PPeditotherdetailsroi(request, ppid, otherdetailsroiid):
    if request.method == 'POST':
        OtherDetailsROI.objects.filter(oth_det_roi_id=otherdetailsroiid).update(
            min_loan_amt = int(request.POST['min_loan_amt']),
            max_loan_amt = int(request.POST['max_loan_amt']),
            min_val = int(request.POST['min_val']),
            max_val = int(request.POST['max_val']),
            roi_men = request.POST['roi_men'],
            roi_women = request.POST['roi_women']
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'otherdetailsroi': OtherDetailsROI.objects.filter(oth_det_roi_id=otherdetailsroiid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editotherdetailsroi.html', context=context)

def PPcostsheet(request, ppid):
    if request.method == 'POST':
        particulars = request.POST.get('particulars')

        CostSheet(particulars=particulars).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/costsheet.html', context=context)

def PPeditcostsheet(request, ppid, costsheetid):
    if request.method == 'POST':
        CostSheet.objects.filter(cost_particular_id=costsheetid).update(
            particulars = request.POST['particulars']
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'costsheet': CostSheet.objects.filter(cost_particular_id=costsheetid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editcostsheet.html', context=context)

def PPProducts(request):
    if request.method == 'POST':
        product = request.POST['prod_name']
        bank = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]

        Products(prod_name=product, bank_id=bank).save()
        return redirect('dashboard')
    context={
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/Products.html', context=context)

def PPcustomerdesignation(request, ppid):
    if request.method == 'POST':
        cust_desig = request.POST['cust_desig']

        CustomerDesignation(cust_desig=cust_desig, bank_id=Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/customerdesignation.html', context=context)

def ppeditcustomerdesignation(request, ppid, customerdesignationid):
    if request.method== 'POST':
        CustomerDesignation.objects.filter(cust_desig_id=customerdesignationid).update(
            cust_desig=request.POST['cust_desig'],
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'customerdesignation': CustomerDesignation.objects.filter(cust_desig_id=customerdesignationid)[0]
    }
    return render(request, 'HomeLoan/editcustomerdesignation.html', context=context)

def PPProperty(request, ppid):
    if request.method == 'POST':
        Property(
            builder_cat      = request.POST['builder_cat'],
            occupation_certi = request.POST['occupation_certi'],
            prev_agreement   = request.POST['prev_agreement'],
            sub_scheme       = request.POST['sub_scheme'],
            perc_completion  = int(request.POST['perc_completion']),
            bank_id          = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)

    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/Property.html', context=context)

def PPeditproperty(request, ppid, propertyid):
    if request.method == 'POST':
        property = Property.objects.filter(prop_id=propertyid)
        property.update(
            builder_cat      = request.POST['builder_cat'],
            occupation_certi = request.POST['occupation_certi'],
            prev_agreement   = request.POST['prev_agreement'],
            sub_scheme       = request.POST['sub_scheme'],
            perc_completion  = int(request.POST['perc_completion']),
        )
        return redirect('editproductandpolicy', ppid)
    context =  {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'pp': ProductsAndPolicy.objects.filter(prod_id=ppid)[0],
        'property': Property.objects.filter(prop_id=propertyid)[0]
    }
    return render(request, 'HomeLoan/editproperty.html', context)


def PPcustomer(request, ppid):
    if request.method == 'POST':
        Customer(
            min_age     = int(request.POST['min_age']),
            total_Exp   = int(request.POST['total_Exp']),
            form16      = request.POST['form16'],
            salary_type = request.POST['salary_type'],
            bank_id     = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', id=ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/customer.html', context=context)

def PPeditcustomer(request, ppid, customerid):
    if request.method == 'POST':
        Customer.objects.filter(cust_id=customerid).update(
            min_age = int(request.POST['min_age']),
            total_Exp = int(request.POST['total_Exp']),
            form16 = request.POST['form16'],
            salary_type = request.POST['salary_type'],
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'customer': Customer.objects.filter(cust_id=customerid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editcustomer.html', context=context)

def PPPropertyType(request, ppid):
    if request.method == 'POST':
        PropertyType(
            prop_type = request.POST['prop_type'],
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', id=ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/PropertyType.html', context=context)

def PPeditPropertyType(request, ppid, propertytypeid):
    if request.method == 'POST':
        PropertyType.objects.filter(prop_type_id=propertytypeid).update(
            prop_type = request.POST['prop_type'],
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'propertytype': PropertyType.objects.filter(prop_type_id=propertytypeid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editpropertytype.html', context=context)

def PPcustomernationality(request, ppid):
    if request.method == 'POST':
        CustomerNationality(
            cust_nat = request.POST['cust_nat'],
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', id=ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/customernationality.html', context=context)

def PPeditcustomernationality(request, ppid, customernationalityid):
    if request.method == 'POST':
        CustomerNationality.objects.filter(cust_nat_id=customernationalityid).update(
            cust_nat = request.POST['cust_nat']
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'customernatnality': CustomerNationality.objects.filter(cust_nat_id=customernationalityid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editcustomernationality.html', context=context)

def PPfees(request, ppid):
    if request.method == 'POST':
        Fees(
            login_fees = request.POST['login_fees'],
            proc_fee_app = request.POST['proc_fee_app'],
            proc_fee_type = request.POST['proc_fee_type'],
            proc_fee_flat_loan_amtwise = request.POST['proc_fee_flat_loan_amtwise'],
            proc_fee_percent_loan_amtwise = request.POST['proc_fee_percent_loan_amtwise'],
            offers = request.POST['offers'],
            offline_or_online = request.POST['offline_or_online'],
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/fees.html', context=context)

def PPeditfee(request, ppid, feeid):
    if request.method == 'POST':
        Fees.objects.filter(fee_id=feeid).update(
            login_fees = request.POST['login_fees'],
            proc_fee_app = request.POST['proc_fee_app'],
            proc_fee_type = request.POST['proc_fee_type'],
            proc_fee_flat_loan_amtwise = request.POST['proc_fee_flat_loan_amtwise'],
            proc_fee_percent_loan_amtwise = request.POST['proc_fee_percent_loan_amtwise'],
            offers = request.POST['offers'],
            offline_or_online = request.POST['offline_or_online'],
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'fee': Fees.objects.filter(fee_id=feeid)[0]
    }
    return render(request, 'HomeLoan/editfee.html', context=context)

def PPRemarks(request, ppid):
    if request.method == 'POST':
        Remarks(
            remark = request.POST['Remarks']
        ).save()
        return redirect('dashboard')
    context={}
    return render(request, 'HomeLoan/Remarks.html', context=context)

def PPincomefoir(request, ppid):
    if request.method == 'POST':
        IncomeFoir(
            min_amt = int(request.POST['min_amt']),
            max_amt = int(request.POST['max_amt']),
            percent = int(request.POST['percent']),
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/incomefoir.html', context=context)

def PPeditincomefoir(request, ppid, incomefoirid):
    if request.method == 'POST':
        IncomeFoir.objects.filter(inc_foir_id=incomefoirid).update(
            min_amt = int(request.POST['min_amt']),
            max_amt = int(request.POST['max_amt']),
            percent = int(request.POST['percent']),

        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'incomefoir': IncomeFoir.objects.filter(inc_foir_id=incomefoirid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editincomefoir.html', context=context)

def PPRoomType(request, ppid):
    if request.method == 'POST':
        RoomType(
            room_type = request.POST['room_type'],
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/RoomType.html', context=context)

def PPediRoomType(request, ppid, roomtypeid):
    if request.method == 'POST':
        RoomType.objects.filter(romm_id=roomtypeid).update(
            room_type = request.POST['room_type']
        )
        return redirect('editproductandpolicy', ppid)
        context = {
            'roomtype': RoomType.objects.filter(romm_id=roomtypeid)[0],
            'product': Products.objects.filter(prod_id=ppid)[0],
        }
        return redirect(request, 'HomeLoan/editroomtype.html', context=context)
    context = {
        'roomtype': RoomType.objects.filter(romm_id=roomtypeid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editroomtype.html', context=context)

def PPincome(request, ppid):
    if request.method == 'POST':
        Income(
            gross_sal                              = request.POST['gross_sal'],
            net_sal                                = request.POST['net_sal'],
            bonus                                  = request.POST['bonus'],
            bonus_avg_yearly                       = request.POST['bonus_avg_yearly'],
            bonus_avg_yearly_percent               = request.POST['bonus_avg_yearly_percent'],
            bonus_avg_qtr                          = request.POST['bonus_avg_qtr'],
            bonus_avg_qtr_percent                  = request.POST['bonus_avg_qtr_percent'],
            bonus_avg_half_yearly                  = request.POST['bonus_avg_half_yearly'],
            bonus_avg_half_yearly_percent          = request.POST['bonus_avg_half_yearly_percent'],
            rent_income                            = request.POST['rent_income'],
            rent_agreement_type                    = request.POST['rent_agreement_type'],
            bank_ref                               = request.POST['bank_ref'],
            rent_ref_in_bank                       = request.POST['rent_ref_in_bank'],
            rent_inc_percent                       = request.POST['rent_inc_percent'],
            fut_rent                               = request.POST['fut_rent'],
            fut_rent_percent                       = request.POST['fut_rent_percent'],
            incentive                              = request.POST['incentive'],
            incen_avg_months                       = request.POST['incen_avg_months'],
            incen_percent                          = request.POST['incen_percent'],
            coApplicant_No_Income_only_Rent_income = request.POST['coApplicant_No_Income_only_Rent_income'],
            bank_id                                = Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/income.html', context=context)

def PPeditincome(request, ppid, incomeid):
    if request.method == 'POST':
        Income.objects.filter(income_id=incomeid).update(
            gross_sal                              = request.POST['gross_sal'],
            net_sal                                = request.POST['net_sal'],
            bonus                                  = request.POST['bonus'],
            bonus_avg_yearly                       = request.POST['bonus_avg_yearly'],
            bonus_avg_yearly_percent               = request.POST['bonus_avg_yearly_percent'],
            bonus_avg_qtr                          = request.POST['bonus_avg_qtr'],
            bonus_avg_qtr_percent                  = request.POST['bonus_avg_qtr_percent'],
            bonus_avg_half_yearly                  = request.POST['bonus_avg_half_yearly'],
            bonus_avg_half_yearly_percent          = request.POST['bonus_avg_half_yearly_percent'],
            rent_income                            = request.POST['rent_income'],
            rent_agreement_type                    = request.POST['rent_agreement_type'],
            bank_ref                               = request.POST['bank_ref'],
            rent_ref_in_bank                       = request.POST['rent_ref_in_bank'],
            rent_inc_percent                       = request.POST['rent_inc_percent'],
            fut_rent                               = request.POST['fut_rent'],
            fut_rent_percent                       = request.POST['fut_rent_percent'],
            incentive                              = request.POST['incentive'],
            incen_avg_months                       = request.POST['incen_avg_months'],
            incen_percent                          = request.POST['incen_percent'],
            coApplicant_No_Income_only_Rent_income = request.POST['coApplicant_No_Income_only_Rent_income'],
        )
        return redirect('editproductandpolicy', ppid)

    context = {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'income': Income.objects.filter(income_id=incomeid)[0]
    }
    return render(request, 'HomeLoan/editincome.html', context=context)

def PPStageOfConstruction(request, ppid):
    if request.method == 'POST':
        StageOfConstruction(
            stage = request.POST['stage'],
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('dashboard')
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/StageOfConstruction.html', context=context)

def PPeditstageofconstruction(request, ppid, stageofconstructionid):
    if request.method == 'POST':
        StageOfConstruction.objects.filter(stage_id=stageofconstructionid).update(
            stage = request.POST['stage'],
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'stageofconstruction': StageOfConstruction.objects.filter(stage_id=stageofconstructionid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editstageofconstruction.html', context=context)

def PPLoanAmount(request, ppid):
    if request.method == 'POST':
        LoanAmount(
            min_loan_amt = int(request.POST['min_loan_amt']),
            max_loan_amt = int(request.POST['max_loan_amt']),
            total_Exp = int(request.POST['total_Exp']),
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/LoanAmount.html', context=context)

def PPeditLoanAmount(request, ppid, loanamountid):
    if request.method == 'POST':
        LoanAmount.objects.filter(loan_id=loanamountid).update(
            min_loan_amt = int(request.POST['min_loan_amt']),
            max_loan_amt = int(request.POST['max_loan_amt']),
            total_Exp = int(request.POST['total_Exp'])
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'loanamount': LoanAmount.objects.filter(loan_id=loanamountid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editloanamount.html', context=context)

def PPLtvResale(request, ppid):
    if request.method == 'POST':
        LtvResale(
            min_amount = request.POST['min_amount'],
            max_amount = request.POST['max_amount'],
            rbi_guidelines = request.POST['rbi_guidelines'],
            doccument_cost = request.POST['doccument_cost'],
            additional = request.POST['additional'],
            car_parking = request.POST['car_parking'],
            total = request.POST['total'],
            market_value = request.POST['market_value'],
            av_capping = request.POST['av_capping'],
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/LtvResale.html', context=context)

def PPeditLtvResale(request, ppid, ltvresaleid):
    if request.method == 'POST':
        LtvResale.objects.filter(ltv_id=ltvresaleid).update(
            min_amount = request.POST['min_amount'],
            max_amount = request.POST['max_amount'],
            rbi_guidelines = request.POST['rbi_guidelines'],
            doccument_cost = request.POST['doccument_cost'],
            additional = request.POST['additional'],
            car_parking = request.POST['car_parking'],
            total = request.POST['total'],
            market_value = request.POST['market_value'],
            av_capping = request.POST['av_capping']
        )
        return redirect('editproductandpolicy', ppid)
    context = {
        'ltvresale': LtvResale.objects.filter(ltv_id=ltvresaleid)[0],
        'product': Products.objects.filter(prod_id=ppid)[0],
    }
    return render(request, 'HomeLoan/editltvresale.html', context=context)

def PPLoantowardsvaluation(request, ppid):
    if request.method == 'POST':
        LoanTowardsValuation(
            cost_sheet = request.POST['cost_sheet'],
            min_amount = int(request.POST['min_amount']),
            max_amount = int(request.POST['max_amount']),
            rbi_guidelines = request.POST['rbi_guidelines'],
            ammenity = request.POST['ammenity'],
            additional = request.POST['additional'],
            car_parking = request.POST['car_parking'],
            car_parking_percent = request.POST['car_parking_percent'],
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)
    context={
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/Loantowardsvaluation.html', context=context)



def PPeditloantowardsvalution(request, ppid, ltvid):
    if request.method == 'POST':
        LoanTowardsValuation.objects.filter(loan_tow_val_id=ltvid).update(
            cost_sheet = request.POST['cost_sheet'],
            min_amount = int(request.POST['min_amount']),
            max_amount = int(request.POST['max_amount']),
            rbi_guidelines = request.POST['rbi_guidelines'],
            ammenity = request.POST['ammenity'],
            additional = request.POST['additional'],
            car_parking = request.POST['car_parking'],
            car_parking_percent = request.POST['car_parking_percent'],
        )

        return redirect('editproductandpolicy', ppid)

    context={
        'ltv': LoanTowardsValuation.objects.filter(loan_tow_val_id=ltvid)[0],
        'pp' : ProductsAndPolicy.objects.filter(prod_id=ppid)[0]
    }
    return render(request, 'HomeLoan/editloantowardsvalution.html', context=context)

def PPotherdetails(request, ppid):
    if request.method == 'POST':
        OtherDetails(
            prevailing_rate = request.POST['prevailingrate'],
            tenure = request.POST['tenure'],
            inward_cheque_return = request.POST['inwardchequereturn'],
            multiple_inquiry = request.POST['multipleinquiry'],
            bank_id= Bank.objects.filter(bank_id=Products.objects.filter(prod_id=ppid)[0].bank_id.bank_id)[0]
        ).save()
        return redirect('editproductandpolicy', ppid)

    context = {
        'product': Products.objects.filter(prod_id=ppid)[0],
        'banks': Bank.objects.all(),
    }
    return render(request, 'HomeLoan/otherdetails.html', context=context)

def ppeditotherdetail(request, ppid, otherdetailid):
    if request.method == 'POST':
        OtherDetails.objects.filter(oth_det_id=otherdetailid).update(
            prevailing_rate = request.POST['prevailingrate'],
            tenure = request.POST['tenure'],
            inward_cheque_return = request.POST['inwardchequereturn'],
            multiple_inquiry = request.POST['multipleinquiry'],
        )
        return redirect('editproductandpolicy', ppid)

    context = {
        'pp': ProductsAndPolicy.objects.filter(prod_id=ppid)[0],
        'otherdetail': OtherDetails.objects.filter(oth_det_id=otherdetailid)[0]
    }
    return render(request, 'HomeLoan/editotherdetails.html', context=context)

def editproductandpolicy(request, id):
    pass


def productsandpolicy(request,action='no'):
    # action = request.GET['action']
    if action == 'edit':
        id = int(action)
        product_and_policy_instance = ProductsAndPolicy.objects.get(pk = id)
        if product_and_policy_instance != 'no':
            productandpolicy_form = ProductsandPolicyForm(instance = product_and_policy_instance)
            if not product_and_policy_instance.lock:
                if request.method == 'POST':
                    current_value_form = ProductsandPolicyForm(request.POST)
                    if current_value_form.is_valid():
                        current_instance = current_value_form.save(commit = False)
                        current_instance.pk = product_and_policy_instance.pk
                        current_instance.save()
                        messages.success(request,"Product And Policy Details Updated Successfully")
                        return redirect("AddProductsAndPolicy", current_instance.pk)
                    else:
                        messages.error(request,current_value_from.errors)
                else:
                    return render(request,'HomeLoan/AddProductsAndPolicy.html',context = {"form":productandpolicy_form,"id":id})
        else:
            return render(request,'HomeLoan/AddProductsAndPolicy.html',context = {"form":ProductsandPolicyForm(),"id":'no'})
    else:
        if request.method == 'POST':
            current_value_form = ProductsandPolicyForm(request.POST)
            if current_value_form.is_valid():
                current_instance = current_value_form.save(commit = False)
                current_instance.save()
                messages.success(request," Products and Policy Details Added Successfully !")
                return redirect('ProductsAndPolicyBasicDetails', current_instance.pk)
            else:
                messages.error(request,current_value_form.errors)
                return redirect('AddProductsAndPolicy', 'new')
        else:
            context = {
                "ProductsandPolicy":ProductsandPolicyForm(),
                "action":'new'
            }
            return render(request,'HomeLoan/ProductsAndPolicy.html',context)


         

    # if request.method == 'POST':
    #     product = Products(
    #         prod_name = request.POST['productname'],
    #         bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #     )
    #     product.save()
    #     if request.POST['min_age'] != '':
    #         Age(
    #             min_age = int(request.POST['min_age']),
    #             retire_age = int(request.POST['retire_age']),
    #             max_age_consi_others = int(request.POST['Max_age_consi_others']),
    #             max_age_consi_gov = int(request.POST['Max_age_consi_others']),
    #             bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #         ).save()

    #     if request.POST['cibil_range_min'] != '':
    #         Cibil(
    #             cibil_range_min = int(request.POST['cibil_range_min']),
    #             cibil_range_max = int(request.POST['cibil_range_max']),
    #             bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #         ).save()

    #     if request.POST['comp_type'] != '':
    #         Company(
    #             comp_type = request.POST['comp_type'],
    #             bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #         ).save()

    #     if request.POST['min_age'] != '':
    #         Customer(
    #             min_age = int(request.POST['min_age']),
    #             total_Exp = int(request.POST['total_exp']),
    #             form16 = request.POST['form16'],
    #             salary_type = request.POST['salary_type'],
    #             bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #         ).save()

    #     if request.POST['cust_desig'] != '':
    #         CustomerDesignation(
    #             cust_desig = request.POST['cust_desig'],
    #             bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #         ).save()

    #     if request.POST['cust_nat'] != '':
    #         CustomerNationality(
    #             cust_nat = request.POST['cust_nat'],
    #             bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #         ).save()

    #     if request.POST['loginfees'] != '':
    #         Fees(
    #             login_fees = request.POST['loginfees'],
    #             proc_fee_app = request.POST['procfeeapp'],
    #             proc_fee_type = request.POST['procfeetype'],
    #             proc_fee_flat_loan_amtwise = request.POST['procfeeflatloanamtwise'],
    #             proc_fee_percent_loan_amtwise = request.POST['procfeepercentloanamtwise'],
    #             offers = request.POST['offers'],
    #             offline_or_online = request.POST['offlineonline'],
    #             bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #         ).save()

    #     if request.POST['grosssal'] != '':
    #         Income(
    #             gross_sal = request.POST['grosssal'],
    #             net_sal = request.POST['netsal'],
    #             bonus = request.POST['bonus'],
    #             bonus_avg_yearly = request.POST['bonus_avg_yearly'],
    #             bonus_avg_yearly_percent = request.POST['bonus_avg_yearly_percent'],
    #             bonus_avg_qtr = request.POST['bonus_avg_qtr'],
    #             bonus_avg_qtr_percent = request.POST['bonus_avg_qtr_percent'],
    #             bonus_avg_half_yearly = request.POST['bonus_avg_half_yearly'],
    #             bonus_avg_half_yearly_percent = request.POST['bonus_avg_half_yearly_percent'],
    #             rent_income = request.POST['rent_income'],
    #             rent_agreement_type = request.POST['rentagreementtype'],
    #             bank_ref = request.POST['bank_ref'],
    #             rent_ref_in_bank = request.POST['rent_ref_in_bank'],
    #             rent_inc_percent = request.POST['rent_inc_percent'],
    #             fut_rent = request.POST['fut_rent'],
    #             fut_rent_percent = request.POST['fut_rent_percent'],
    #             incentive = request.POST['incentive'],
    #             incen_avg_months = request.POST['incen_avg_months'],
    #             incen_percent = request.POST['incen_percent'],
    #             coApplicant_No_Income_only_Rent_income = request.POST['coApplicant_No_Income_only_Rent_income'],
    #             bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #         ).save()

    #         if request.POST['min_amt'] != '':
    #             IncomeFoir(
    #                 min_amt = int(request.POST['min_amt']),
    #                 max_amt = int(request.POST['max_amt']),
    #                 percent = int(request.POST['percent']),
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['min_loan_amt'] != '':
    #             LoanAmount(
    #                 min_loan_amt = int(request.POST['min_loan_amt']),
    #                 max_loan_amt = int(request.POST['max_loan_amt']),
    #                 total_Exp = int(request.POST['total_exp']),
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['cost_sheet'] != '':
    #             LoanTowardsValuation(
    #                 cost_sheet = request.POST['cost_sheet'],
    #                 min_amount = int(request.POST['min_amount']),
    #                 max_amount = int(request.POST['max_amount']),
    #                 rbi_guidelines = request.POST['rbi_guideline'],
    #                 ammenity = request.POST['ammenity'],
    #                 additional = request.POST['additional'],
    #                 car_parking = request.POST['car_parking'],
    #                 car_parking_percent = request.POST['car_parking_parcent'],
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['min_amount'] != '':
    #             LtvResale(
    #                 min_amount = int(request.POST['min_amount']),
    #                 max_amount = int(request.POST['max_amount']),
    #                 rbi_guidelines = int(request.POST['ltvrbi_guideline']),
    #                 doccument_cost = int(request.POST['doccument_cost']),
    #                 additional = int(request.POST['additional']),
    #                 car_parking = int(request.POST['car_parking']),
    #                 total = int(request.POST['total']),
    #                 market_value = int(request.POST['market_value']),
    #                 av_capping = int(request.POST['av_capping']),
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['neg_emp_pro'] != '':
    #             NegativeEmployerProfile(
    #                 neg_emp_pro = request.POST['neg_emp_pro'],
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['neg_area'] != '':
    #             NegativeArea(
    #                 neg_area = request.POST['neg_area'],
    #                 bank_id  = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['emioblig'] != '':
    #             Obligation(
    #                 emi_oblig = request.POST['emioblig'],
    #                 emi_oblig_not_consi = request.POST['emioblignotconsidered'],
    #                 credit_card = request.POST['creditcard'],
    #                 credit_card_oblig_percent = int(request.POST['creditcardobligperc']),
    #                 gold_loan = request.POST['goldloan'],
    #                 gold_loan_percent = int(request.POST['goldloanpercent']),
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['prevailingrate'] != '':
    #             OtherDetails(
    #                 prevailing_rate = int(request.POST['prevailingrate']),
    #                 tenure = request.POST['tenur'],
    #                 inward_cheque_return = request.POST['inwardchequereturn'],
    #                 multiple_inquiry = request.POST['multipleinquiry'],
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['min_loan_amt'] != '':
    #             OtherDetailsROI(
    #                 min_loan_amt = int(request.POST['min_loan_amt']),
    #                 max_loan_amt = int(request.POST['max_loan_amt']),
    #                 min_val = int(request.POST['min_val']),
    #                 max_val = int(request.POST['max_val']),
    #                 roi_women = request.POST['roi_women'],
    #                 roi_men = request.POST['roi_men'],
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['buildercategory'] != '':
    #             Property(
    #                 builder_cat = request.POST['buildercategory'],
    #                 occupation_certi = request.POST['occupationcerti'],
    #                 prev_agreement = request.POST['previousagreement'],
    #                 sub_scheme = request.POST['subscheme'],
    #                 perc_completion = int(request.POST['perccompletion']),
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['prop_type'] != '':
    #             PropertyType(
    #                 prop_type = request.POST['prop_type'],
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['room_type'] != '':
    #             RoomType(
    #                 room_type = request.POST['room_type'],
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()

    #         if request.POST['stage'] != '':
    #             StageOfConstruction(
    #                 stage = request.POST['stage'],
    #                 bank_id = Bank.objects.filter(bank_id=int(request.POST['bank']))[0]
    #             ).save()


    #     return redirect('editproductandpolicy', id=product.prod_id)

    # context = {
    #     'banks': Bank.objects.all(),
    # }

def productsandpolicy_basicdetails(request,id):
    if request.method == 'POST':
        previous_instance = HlBasicDetails.objects.filter(pid = id).first()
        if previous_instance is not None:
            if previous_instance.effective_date is not None:
                if previous_instancec.ineffective_date is not None or previous_instance.ineffective_date >= datetime.now():
                    messages.error(request,"Cannot Change Or Add Basic Details Please check previous effective or ineffective Date")
                    return redirect('listproductandpolicy')
                else:
                    current_value_form = HlBasicDetailsForm(request.POST)
                    if current_value_form.is_valid():
                        current_instance = current_value_form.save(commit = False)
                        current_instance.pk = previous_instance.pk
                        current_instance.save()
                        message.success(request,'Basic Details Updated Successfully')
                    else:
                        messages.error(request,current_value_form.errors)
        current_value_form = HlBasicDetailsForm(request.POST)
        if current_value_form.is_valid():
            current_instance = current_value_form.save(commit = False)
            current_instance.pid = ProductsAndPolicy.objects.get(pk=id)
            current_instance.save()
            messages.success(request,"Basic Details Added Successfully !")
            return redirect('ProductsAndPolicyIncomeDetails',id)
        else:
            messages.error(request,current_value_form.errors)
            return redirect('ProductsAndPolicyBasicDetails', id)
    else:
        if ProductsAndPolicy.objects.filter(pk=id):
            context={
                "basic_details_form" : HlBasicDetailsForm(),
                "id" : id
            }
            return render(request,"HomeLoan/pap_basicdetailsform.html",context)
        else:
            return redirect('listproductandpolicy')

def productsandpolicy_incomedetails(request,id):
    if request.method == 'POST':
        previous_instance = HlIncome.objects.filter(pid = id).first()
        if previous_instance is not None:
            messages.error(request,"Income Details is Already Added. If you want to change then please change it during 'Review or Edit'.")
            return redirect('ProductsAndPolicyIncomeFoirDetails',id)
        else:
            income_details_form = HlIncomeForm(request.POST)
            if income_details_form.is_valid():
                income_instance = income_details_form.save(commit = False)
                income_instance.pid = ProductsAndPolicy.objects.get(pk=id)
                income_instance.save()
                messages.success(request," Income Details Added Successfully !")
                return redirect('ProductsAndPolicyIncomeFoirDetails', id)
            else:
                messages.error(request,income_details_form.errors)
                return redirect('ProductsAndPolicyIncomeDetails', id)
    else:
        if ProductsAndPolicy.objects.filter(pk=id):
            context={
                "income_details_form" : HlIncomeForm(),
                "id" : id
            }
            return render(request,"HomeLoan/pap_incomedetailsform.html",context)
        else:
            return redirect('listproductandpolicy')

def productsandpolicy_incomefoirdetails(request,id):
    if request.method == 'POST':
        if 'next' in request.POST:
            if HlIncomeFoir.objects.filter(pid = id).exists():
                return redirect('ProductsAndPolicyObligationDetails', id)
            else:
                messages.warning(request,'Income Foir Details is not added. Please add Income Foir Details.')
                return redirect('ProductsAndPolicyIncomeFoirDetails', id)
        income_foir_details_form = HlIncomeFoirForm(request.POST)
        if income_foir_details_form.is_valid():
            income_foir_instance = income_foir_details_form.save(commit = False)
            income_foir_instance.pid = ProductsAndPolicy.objects.get(pk=id)
            income_foir_instance.save()
            url = request.POST.get('url')
            messages.success(request,"Income Foir Details Added Successfully !")
            if url:
                return redirect('ProductsAndPolicyReviewOrEdit',id)
            
            else:
                return redirect('ProductsAndPolicyIncomeFoirDetails', id)
        else:
            messages.error(request,income_foir_details_form.errors)
            return redirect('ProductsAndPolicyIncomeFoirDetails', id)
    else:
        if ProductsAndPolicy.objects.filter(pk=id):
            income_foir_instances = HlIncomeFoir.objects.filter(pid = id)
            context={
                "income_foir_details_form" : HlIncomeFoirForm(),
                "id" : id,
                "income_foir_instances" : income_foir_instances
            }
            return render(request,"HomeLoan/pap_incomefoirdetailsform.html",context)
        else:
            return redirect('listproductandpolicy')

def deleteincomefoirdetails(request,id):
    instance = HlIncomeFoir.objects.get(pk=id)
    instance.delete()
    messages.success(request,"Income Foir Details Deleted Successfully !")
    return redirect('ProductsAndPolicyIncomeFoirDetails',instance.pid.pk)

def productsandpolicy_obligation(request,id):
    if not HlIncomeFoir.objects.filter(pid = id).exists():
        messages.error(request,"Income Foir Details is not added. Please add Income Foir Details.")
        return redirect('ProductsAndPolicyIncomeFoirDetails', id)

    if request.method == 'POST':
        previous_instance = HlObligation.objects.filter(pid = id)
        if previous_instance:
            messages.error(request,"Please Edit Obligation Details during review option")
            return redirect('ProductsAndPolicyOtherDetails',id)
        obligation_details_form = HlObligationForm(request.POST)
        if obligation_details_form.is_valid():
            obligation_instance = obligation_details_form.save(commit = False)
            obligation_instance.pid = ProductsAndPolicy.objects.get(pk=id)
            obligation_instance.save()
            messages.success(request,"Obligation Details Added Successfully ! ")
            return redirect('ProductsAndPolicyOtherDetails',id)
        else:
            messages.error(request,obligation_details_form.errors)
            return redirect('ProductsAndPolicyObligationDetails',id)
    else:
        if ProductsAndPolicy.objects.filter(pk=id):
            context={
                "obligation_details_form" : HlObligationForm(),
                "id" : id
            }
            return render(request,"HomeLoan/pap_obligationdetailsform.html",context)
        else:
            return redirect('listproductandpolicy')

def productsandpolicy_otherdetails(request,id):
    if request.method == 'POST':
        other_details_form = HlOtherDetailsForm(request.POST)
        previous_instance = HlOtherDetails.objects.filter(pid = id )
        if previous_instance:
            messages.error(request,"Please Edit Other Details during review option")
            return redirect('ProductsAndPolicyPropertyDetails',id)
        if other_details_form.is_valid():
            other_details_instance = other_details_form.save(commit = False)
            other_details_instance.pid = ProductsAndPolicy.objects.get(pk=id)
            other_details_instance.save()
            messages.success(request,"Other Details Added Successfully ! ")
            return redirect('ProductsAndPolicyPropertyDetails',id)
        else:
            messages.error(request,other_details_form.errors)
            return redirect('ProductsAndPolicyOtherDetails',id)
    else:
        if ProductsAndPolicy.objects.filter(pk=id):
            context={
                "other_details_form" : HlOtherDetailsForm(),
                "id" : id
            }
            return render(request,"HomeLoan/pap_otherdetailsform.html",context) 
        else:
            return redirect('listproductandpolicy')

def productsandpolicy_propertydetails(request,id):
    if request.method == 'POST':
        property_details_form = HlPropertyForm(request.POST)
        if property_details_form.is_valid():
            previous_instance = HlProperty.objects.filter(pid = id)
            if previous_instance:
                messages.error(request,"Please Edit Property Details during review option")
                return redirect('ProductsAndPolicyLoanToValue1Details',id)
            property_details_instance = property_details_form.save(commit = False)
            property_details_instance.pid = ProductsAndPolicy.objects.get(pk=id)
            property_details_instance.save()
            messages.success(request,"Property Details Added Successfully ! ")
            return redirect('ProductsAndPolicyLoanToValue1Details',id)
        else:
            messages.error(request,other_details_form.errors)
            return redirect('ProductsAndPolicyPropertyDetails',id)
    else:
        if ProductsAndPolicy.objects.filter(pk=id):
            context={
                "property_details_form" : HlPropertyForm(),
                "id" : id
            }
            return render(request,"HomeLoan/pap_propertydetailsform.html",context) 
        else:
            return redirect('listproductandpolicy')

def productsandpolicy_loantovalue_1_details(request,id):
    if request.method == 'POST':
        previous_instance = HlLoan_To_Value_Type_1.objects.filter(pid = id)
        if previous_instance:
            messages.error(request,"Loan To Value Type 1 Details is already added. Please edit Loan To Value Type 1 Details during 'Review Or Edit' .")
            return redirect('ProductsAndPolicyLoanToValue2Details',id)
        form = HlLoan_To_Value_Type_1Form(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.pid = ProductsAndPolicy.objects.get(pk = id)
            instance.save()
            messages.success(request,"Loan To Value - Fresh Details Added Successfully ! ")
            return redirect('ProductsAndPolicyLoanToValue2Details',id)
        else:
            messages.error(request,form.errors)
            return redirect('ProductsAndPolicyLoanToValue1Details',id)
    else:
        form = HlLoan_To_Value_Type_1Form()
        action = 'Type1'
        title = 'Underconstruction & Ready Possession from Builder'
        context={
            "form" : form,
            "action" : action,
            "title" : title,
            "id" : id
        }
        return render(request,"HomeLoan/pap_loantovaluedetailsform.html",context)


def productsandpolicy_loantovalue_2_details(request,id):
    if request.method == 'POST':
        previous_instance = HlLoan_To_Value_Type_2.objects.filter(pid = id)
        if previous_instance:
            messages.error(request,"Resale is already added. Please edit Resale Details during 'Review Or Edit' .")
            return redirect('ProductsAndPolicyCibilDetails',id)
        form = HlLoan_To_Value_Type_2Form(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.pid = ProductsAndPolicy.objects.get(pk = id)
            instance.save()
            messages.success(request,"Loan To Value - Resale Details Added Successfully ! ")
            return redirect('ProductsAndPolicyCibilDetails',id)
        else:
            messages.error(request,form.errors)
            return redirect('ProductsAndPolicyLoanToValue2Details',id)
    else:
        form = HlLoan_To_Value_Type_2Form()
        action = 'Type1'
        title = 'Resale'
        context={
            "form" : form,
            "id" : id,
            "action" : action,
            "title" : title
        }
        return render(request,"HomeLoan/pap_loantovalue2detailsform.html",context)


def productsandpolicy_cibildetails(request,id):
    if request.method == 'POST':
        cibil_form_instance = CibilForm(request.POST)
        previous_instance = Cibil.objects.filter(pid = id)
        if previous_instance:
            messages.error(request,'Cibil Details is already added. Please edit Cibil Details during "Review Or Edit"  ')
            return redirect('ProductsAndPolicyReviewOrEdit',id)
        if cibil_form_instance.is_valid():
            cibil_instance = cibil_form_instance.save(commit = False)
            cibil_instance.pid =  ProductsAndPolicy.objects.get(pk=id)
            cibil_instance.save()
            messages.success(request,"Cibil Details Added Successfully ! ")
            return redirect('ProductsAndPolicyReviewOrEdit',id)
        else:
            messages.error(request,cibil_form_instance.errors)
            return redirect('ProductsAndPolicyCibilDetails',id)
    else:
        if ProductsAndPolicy.objects.filter(pk=id):
            cibil_form = CibilForm()
            return render(request,'HomeLoan/pap_cibildetails.html',context = {"id":id,"cibil_form":cibil_form})
        else:
            return redirect('listproductandpolicy')

def productsandpolicy_revieworedit(request,id):
    if not ProductsAndPolicy.objects.filter(pk=id).exists():
        messages.error(request,'No product and policy Found')
        return redirect('listproductandpolicy')
    product_and_policy_instance      = ProductsAndPolicy.objects.get(pk = id)
    hl_basicdetails_instance         = HlBasicDetails.objects.filter(pid = id)
    hl_income_instance               = HlIncome.objects.filter(pid=product_and_policy_instance)
    hl_income_foir_instance          = HlIncomeFoir.objects.filter(pid=product_and_policy_instance)
    cibil_details                    = Cibil.objects.filter(pid = product_and_policy_instance)
    hl_other_details_instance        = HlOtherDetails.objects.filter(pid = product_and_policy_instance)
    hl_obligations_instance          = HlObligation.objects.filter(pid = product_and_policy_instance)
    hl_property_instance             = HlProperty.objects.filter(pid = product_and_policy_instance)
    hl_loan_to_value_type_1_instance = HlLoan_To_Value_Type_1.objects.filter(pid = product_and_policy_instance)
    hl_loan_to_value_type_2_instance = HlLoan_To_Value_Type_2.objects.filter(pid = product_and_policy_instance)
    hl_otherdetails_instance         = HlOtherDetails.objects.filter(pid = product_and_policy_instance)
    product_and_policy_form          = ProductsandPolicyForm(instance = product_and_policy_instance)
    hl_basicdetails_form             = HlBasicDetailsForm(instance = hl_basicdetails_instance.first())
    hl_cibildetails_form             = CibilForm(instance = cibil_details.first())
    hl_obligations_form              = HlObligationForm(instance = hl_obligations_instance.first())
    hl_property_form                 = HlPropertyForm(instance = hl_property_instance.first())
    hl_income_form                   = HlIncomeForm(instance = hl_income_instance.first())
    hl_otherdetails_form             = HlOtherDetailsForm(instance = hl_other_details_instance.first())
    hl_income_foir_form              = HlIncomeFoirForm()
    hl_loan_to_value_type_1_form     = HlLoan_To_Value_Type_1Form(instance = hl_loan_to_value_type_1_instance.first())
    hl_loan_to_value_type_2_form     = HlLoan_To_Value_Type_2Form(instance = hl_loan_to_value_type_2_instance.first())
    context                          = {
        "id"                              : id,
        "hl_basicdetails_instance"        : hl_basicdetails_instance,
        "hl_income_instance"              : hl_income_instance,
        "hl_income_foir_instance"         : hl_income_foir_instance,
        "hl_cibil_details_instance"       : cibil_details,
        "hl_obligations_instance"         : hl_obligations_instance,
        "hl_property_instance"            : hl_property_instance,
        "hl_loan_to_value_type_1_instance": hl_loan_to_value_type_1_instance,
        "hl_loan_to_value_type_2_instance": hl_loan_to_value_type_2_instance,
        "hl_other_details_instance"       : hl_otherdetails_instance,
        "product_and_policy_instance"     : product_and_policy_instance,
        "product_and_policy_form"         : product_and_policy_form,
        "hl_basicdetails_form"            : hl_basicdetails_form,
        "hl_cibildetails_form"            : hl_cibildetails_form,
        "hl_obligations_form"             : hl_obligations_form,
        "hl_property_form"                : hl_property_form,
        "hl_income_form"                  : hl_income_form,
        "hl_incomefoirdetails_form"       : hl_income_foir_form,
        "hl_loan_to_value_type_1_form"    : hl_loan_to_value_type_1_form,
        "hl_loan_to_value_type_2_form"    : hl_loan_to_value_type_2_form,
        "hl_otherdetails_form"            : hl_otherdetails_form,
    }
    return render(request, 'HomeLoan/editproductandpolicy.html', context)

def editbasicdetails(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = HlBasicDetails.objects.get(pk = instance_id)
        hl_basicdetails_form = HlBasicDetailsForm(request.POST)
        if hl_basicdetails_form.is_valid():
            hl_basicdetails_instances_active = HlBasicDetails.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_basicdetails_instances_active) > 0 or len( HlBasicDetails.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Basic Details Please Make current Basic Details Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_basicdetails_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Basic Details Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_basicdetails_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)

    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        hl_basicdetails_instance = HlBasicDetails.objects.get(pk = id)
        if action == 'edit':
            hl_basicdetails_form = HlBasicDetailsForm(instance = hl_basicdetails_instance)
            return render(request,'HomeLoan/editbasicdetails.html',context = {"hl_basicdetails_form":hl_basicdetails_form})
        else:
            hl_basicdetails_instance.ineffective_date = datetime.now()
            hl_basicdetails_instance.save()
            hl_basicdetails_instance.ineffective_date = None
            if hl_basicdetails_instance.ineffective_date is None:
                messages.warning(request,"Basic Details Made Ineffective Please enter new Details ! ")
            else:
                messages.warning(request,"Basic Details Made Ineffective Please enter new Details !  !")
            hl_basicdetails_form = HlBasicDetailsForm(instance = hl_basicdetails_instance)
            return render(request,'HomeLoan/editbasicdetails.html',context = {"hl_basicdetails_form":hl_basicdetails_form})


def editobligations(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = HlObligation.objects.get(pk = instance_id)
        hl_obligations_form = HlObligationForm(request.POST)
        if hl_obligations_form.is_valid():
            hl_obligations_instances_active = HlObligation.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_obligations_instances_active) > 0 or len( HlObligation.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Obligations Please Make current Obligations Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_obligations_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Obligations Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_obligations_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',basic_details_id.pid.pk)
    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        hl_obligations_instance = HlObligation.objects.get(pk = id)
        if action == 'edit':
            hl_obligations_form = HlObligationForm(instance = hl_obligations_instance)
            return render(request,'HomeLoan/editobligationdetails.html',context = {"hl_obligations_form":hl_obligations_form})
        else:
            hl_obligations_instance.ineffective_date = datetime.now()
            hl_obligations_instance.save()
            hl_obligations_instance.ineffective_date = None
            if hl_obligations_instance.ineffective_date is None:
                messages.warning(request,"Obligations Made Ineffective Please enter new Details ! ")
            else:
                messages.warning(request,"Obligations Was Already Ineffective !")
            hl_obligations_form = HlObligationForm(instance = hl_obligations_instance)
            return render(request,'HomeLoan/editobligationdetails.html',context = {"hl_obligations_form":hl_obligations_form})

def editincomedetails(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = HlIncome.objects.get(pk = instance_id)
        hl_incomedetails_form = HlIncomeForm(request.POST)
        if hl_incomedetails_form.is_valid():
            hl_incomedetails_instances_active = HlIncome.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_incomedetails_instances_active) > 0 or len( HlIncome.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Income Details Please Make current Income Details Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_incomedetails_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Income Details Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_incomedetails_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)

    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        hl_income_instance = HlIncome.objects.get(pk = id)
        if action == 'edit':
            hl_income_form = HlIncomeForm(instance = hl_income_instance)
            return render(request,'HomeLoan/editincomedetails.html',context = {"hl_income_form":hl_income_form})
        else:
            hl_income_instance.ineffective_date = datetime.now()
            hl_income_instance.save()
            hl_income_instance.ineffective_date = None
            if hl_income_instance.ineffective_date is None:
                messages.warning(request,"Income Details Made Ineffective Please enter new Details ! ")
            else:
                messages.warning(request,"Income Details Was Already Ineffective !")
            hl_income_form = HlIncomeForm(instance = hl_income_instance)
            return render(request,'HomeLoan/editincomedetails.html',context = {"hl_income_form":hl_income_form})

def editotherdetails(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = HlOtherDetails.objects.get(pk = instance_id)
        hl_otherdetails_form = HlOtherDetailsForm(request.POST)
        if hl_otherdetails_form.is_valid():
            hl_otherdetails_instances_active = HlOtherDetails.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_otherdetails_instances_active) > 0 or len( HlOtherDetails.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Other Details Please Make current Other Details Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_otherdetails_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Other Details Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_otherdetails_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)

    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        hl_otherdetails_instance = HlOtherDetails.objects.get(pk = id)
        if action == 'edit':
            hl_otherdetails_form = HlOtherDetailsForm(instance = hl_otherdetails_instance)
            return render(request,'HomeLoan/editotherdetails.html',context = {"hl_otherdetails_form":hl_otherdetails_form})
        else:
            hl_otherdetails_instance.ineffective_date = datetime.now()
            hl_otherdetails_instance.save()
            hl_otherdetails_instance.ineffective_date = None
            if hl_otherdetails_instance.ineffective_date is None:
                messages.warning(request,"Other Details Made Ineffective Please enter new Details ! ")
            else:
                messages.warning(request,"Other Details Was Already Ineffective !")
            hl_otherdetails_form = HlOtherDetailsForm(instance = hl_otherdetails_instance)
            return render(request,'HomeLoan/editotherdetails.html',context = {"hl_otherdetails_form":hl_otherdetails_form})
        

def editpropertydetails(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = HlProperty.objects.get(pk = instance_id)
        hl_propertydetails_form = HlPropertyForm(request.POST)
        if hl_propertydetails_form.is_valid():
            hl_propertydetails_instances_active = HlProperty.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_propertydetails_instances_active) > 0 or len( HlProperty.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Property Details Please Make current Property Details Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_propertydetails_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Property Details Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_propertydetails_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)

    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        hl_property_instance = HlProperty.objects.get(pk = id)
        if action == 'edit':
            hl_property_form = HlPropertyForm(instance = hl_property_instance)
            return render(request,'HomeLoan/editpropertydetails.html',context = {"hl_property_form":hl_property_form})
        else:
            hl_property_instance.ineffective_date = datetime.now()
            hl_property_instance.save()
            hl_property_instance.ineffective_date = None
            if hl_property_instance.ineffective_date is None:
                messages.warning(request,"Property Details Made Ineffective Please enter new Details ! ")
            else:
                messages.warning(request,"Property Details Was Already Ineffective !")
            hl_property_form = HlPropertyForm(instance = hl_property_instance)
            return render(request,'HomeLoan/editpropertydetails.html',context = {"hl_property_form":hl_property_form})

def editincomefoirdetails(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = HlIncomeFoir.objects.get(pk = instance_id)
        hl_incomeforeclosure_form = HlIncomeFoirForm(request.POST)
        if hl_incomeforeclosure_form.is_valid():
            hl_incomeforeclosure_instances_active = HlIncomeFoir.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_incomeforeclosure_instances_active) > 0 or len( HlIncomeFoir.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Income Foir Details Please Make current Income Foir Details Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_incomeforeclosure_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Income Foir Details Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_incomeforeclosure_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)

    if request.method == 'GET':
        instance_id = request.GET.get('id')
        action = request.GET.get('action')
        hl_incomefoirdetails_instance = HlIncomeFoir.objects.get(pk = instance_id)
        if action == 'edit':
            hl_incomefoirdetails_form = HlIncomeFoirForm(instance = hl_incomefoirdetails_instance)
            return render(request,'HomeLoan/editincomefoirdetails.html',context = {"hl_incomefoirdetails_form":hl_incomefoirdetails_form})
        else:
            hl_incomefoirdetails_instance.ineffective_date = datetime.now()
            hl_incomefoirdetails_instance.save()
            hl_incomefoirdetails_instance.ineffective_date = None
            if hl_incomefoirdetails_instance.ineffective_date is None:
                messages.warning(request,"Income Foir Details Made Ineffective Please enter new Details ! ")
            else:
                messages.warning(request,"Income Foir Details Was Already Ineffective !")
            hl_incomefoirdetails_form = HlIncomeFoirForm(instance = hl_incomefoirdetails_instance)
            return render(request,'HomeLoan/editincomefoirdetails.html',context = {"hl_incomefoirdetails_form":hl_incomefoirdetails_form})

def editloantovaluedetails(request):
    if request.method == 'GET':
        instance_id = request.GET.get('id')
        action = request.GET.get('action')
        type = request.GET.get('property_type')
        if type == 'type_1':
            hl_loantovalue_instance = HlLoan_To_Value_Type_1.objects.get(pk = instance_id)
        else:
            hl_loantovalue_instance = HlLoan_To_Value_Type_2.objects.get(pk = instance_id)
        if action == 'edit':
            if type == 'type_1':
                hl_loantovalue_form = HlLoan_To_Value_Type_1Form(instance = hl_loantovalue_instance)
                return render(request,'HomeLoan/editloantovaluedetails.html',context = {"hl_loantovalue1_form":hl_loantovalue_form})
            else:
                hl_loantovalue_form = HlLoan_To_Value_Type_2Form(instance = hl_loantovalue_instance)
                return render(request,'HomeLoan/editloantovaluedetails.html',context = {"hl_loantovalue2_form":hl_loantovalue_form})
        else:
            hl_loantovalue_instance.ineffective_date = datetime.now()
            hl_loantovalue_instance.save()
            hl_loantovalue_instance.ineffective_date = None
            messages.warning(request,"Loan To Value Details Made Ineffective !")
            if type == 'type_1':
                hl_loantovalue_form = HlLoan_To_Value_Type_1Form(instance = hl_loantovalue_instance)
                return render(request,'HomeLoan/editloantovaluedetails.html',context = {"hl_loantovalue1_form":hl_loantovalue_form})
            else:
                hl_loantovalue_form = HlLoan_To_Value_Type_2Form(instance = hl_loantovalue_instance)
                return render(request,'HomeLoan/editloantovaluedetails.html',context = {"hl_loantovalue2_form":hl_loantovalue_form})                

def editcibildetails(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = Cibil.objects.get(pk = instance_id)
        hl_cibil_form = CibilForm(request.POST)
        if hl_cibil_form.is_valid():
            hl_cibil_instances_active = Cibil.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_cibil_instances_active) > 0 or len( Cibil.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Cibil Details Please Make current Cibil Details Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_cibil_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Cibil Details Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_cibil_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        hl_cibildetails_instance = Cibil.objects.get(pk = id)
        if action == 'edit':
            hl_cibildetails_form = CibilForm(instance = hl_cibildetails_instance)
            return render(request,'HomeLoan/editCibil.html',context = {"hl_cibildetails_form":hl_cibildetails_form})
        else:
            hl_cibildetails_instance.ineffective_date = datetime.now()
            hl_cibildetails_instance.save()
            hl_cibildetails_instance.ineffective_date = None
            messages.warning(request,"Cibil Details Made Ineffective Please enter new Details ! ")
            hl_cibildetails_form = CibilForm(instance = hl_cibildetails_instance)
            return render(request,'HomeLoan/editCibil.html',context = {"hl_cibildetails_form":hl_cibildetails_form})

def editloanvaluetype1(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = HlLoan_To_Value_Type_1.objects.get(pk = instance_id)
        hl_loantovalue1_form = HlLoan_To_Value_Type_1Form(request.POST)
        if hl_loantovalue1_form.is_valid():
            hl_loantovalue1_instances_active = HlLoan_To_Value_Type_1.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_loantovalue1_instances_active) > 0 or len( HlLoan_To_Value_Type_1.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Loan To Value Details Please Make current Loan To Value Details Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_loantovalue1_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Loan To Value Details Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_loantovalue1_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)

    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        hl_type1_instance = HlLoan_To_Value_Type_1.objects.get(pk = id)
        if action == 'edit':
            hl_type1_form = HlLoan_To_Value_Type_1Form(instance = hl_type1_instance)
            return render(request,'HomeLoan/editloantovaluetype1.html',context = {"hl_type1_form":hl_type1_form})
        else:
            hl_type1_instance.ineffective_date = datetime.now()
            hl_type1_instance.save()
            hl_type1_instance.ineffective_date = None
            messages.warning(request,"Loan To Value Details Made Ineffective !")
            hl_type1_form = HlLoan_To_Value_Type_1Form(instance = hl_type1_instance)
            return render(request,'HomeLoan/editloantovaluetype1.html',context = {"hl_type1_form":hl_type1_form})

def editloanvaluetype2(request):
    if request.method == 'POST':
        instance_id = request.POST.get('id')
        instance = HlLoan_To_Value_Type_2.objects.get(pk = instance_id)
        hl_loantovalue2_form = HlLoan_To_Value_Type_2Form(request.POST)
        if hl_loantovalue2_form.is_valid():
            hl_loantovalue2_instances_active = HlLoan_To_Value_Type_2.objects.filter(ineffective_date__gte = datetime.now(),effective_date__isnull = False)
            if len(hl_loantovalue2_instances_active) > 0 or len( HlLoan_To_Value_Type_2.objects.filter(ineffective_date__isnull= True,effective_date__isnull = False)):
                messages.error(request,'Cannot Edit Loan To Value Details Please Make current Loan To Value Details Ineffective')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
            else:
                current_instance = hl_loantovalue2_form.save(commit = False)
                current_instance.pid = instance.pid
                if instance.effective_date == None:
                    current_instance.pk = instance.pk
                current_instance.save()
                messages.success(request,'Loan To Value Details Edited Successfully')
                return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
        else:
            messages.error(request,hl_loantovalue2_form.errors)
            return redirect('ProductsAndPolicyReviewOrEdit',instance.pid.pk)
    
    if request.method == 'GET':
        id = request.GET.get('id')
        action = request.GET.get('action')
        hl_type2_instance = HlLoan_To_Value_Type_2.objects.get(pk = id)
        if action == 'edit':
            hl_type2_form = HlLoan_To_Value_Type_2Form(instance = hl_type2_instance)
            return render(request,'HomeLoan/editloantovaluetype2.html',context = {"hl_type2_form":hl_type2_form})
        else:
            hl_type2_instance.ineffective_date = datetime.now()
            hl_type2_instance.save()
            hl_type2_instance.ineffective_date = None
            messages.warning(request,"Loan To Value Details Made Ineffective !")
            hl_type2_form = HlLoan_To_Value_Type_2Form(instance = hl_type2_instance)
            return render(request,'HomeLoan/editloantovaluetype2.html',context = {"hl_type2_form":hl_type2_form})

@login_required (redirect_field_name='login', login_url='login')
def listproductandpolicy(request):
    context = {
        'ProductsAndPolicy': ProductsAndPolicy.objects.all()
    }
    return render(request, 'HomeLoan/listproductsandpolicy.html', context=context)

def submitproductandpolicy(request,id):
    pass
    # productandpolicy = ProductsAndPolicy.objects.filter(pk = id)
    # if productandpolicy is None:
    #     messages.error(reqeust,'Product And Policy Not Found')
    #     return redirect('listproductandpolicy')
    # else:
    #     productandpolicy = productandpolicy[0]
        