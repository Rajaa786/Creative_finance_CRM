from bdb import effective
from urllib import request
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from stronghold.decorators import public

# Create your views here.


def CompanyName_form(request):
    if request.method == "POST":
        companynameformvalue = request.POST["CompanyName"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["CompanyNameIdate"]
        if CompanyName.objects.filter(company_name=companynameformvalue).exists():
            messages.info(request, "Company Name already exists")
            return redirect("Master_details")
        else:
            newcompanytype = CompanyName.objects.create(
                company_name=companynameformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newcompanytype.save()
            return redirect("Master_details")

    return render(request, "master/master_details.html")


def CompanyType_form(request):
    if request.method == "POST":
        companytypeformvalue = request.POST["CompanyType"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["CompanyTypeIdate"]
        if CompanyType.objects.filter(company_type=companytypeformvalue).exists():
            messages.info(request, "Company Type already exists")
            return redirect("Master_details")
        else:
            newcompanytype = CompanyType.objects.create(
                company_type=companytypeformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newcompanytype.save()
            return redirect("Master_details")

    return render(request, "master/master_details.html")


def CompanyCat_form(request):
    if request.method == "POST":
        companycatformvalue = request.POST["CompanyCat"].strip()
        if CompanyCatergoryTypes.objects.filter(
            company_cat=companycatformvalue
        ).exists():
            messages.info(request, "Company Category already exists")
            return redirect("Master_details")
        else:
            newcompanycat = CompanyCatergoryTypes.objects.create(
                cocat_type=companycatformvalue
            )
            newcompanycat.save()
            return redirect("Master_details")

    return render(request, "master/master_details.html")


def Tenure_form(request):
    if request.method == "POST":
        tenureformvalue = request.POST["Tenure"].strip()
        if Tenure.objects.filter(ten_type=tenureformvalue).exists():
            messages.info(request, "Tenure already exists")
            return redirect("Master_details")
        else:
            newtenure = Tenure.objects.create(ten_type=tenureformvalue)
            newtenure.save()
            return redirect("Master_details")

    return render(request, "master/master_details.html")


def Agreementtype_form(request):
    if request.method == "POST":
        agreementtypeformvalue = request.POST["AgreementType"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["AgreementtypeIdate"]
        if AgreementType.objects.filter(agreement_type=agreementtypeformvalue).exists():
            messages.info(request, "Agreement Type already exists")
            return redirect("Master_details")
        else:
            newagreementtype = AgreementType.objects.create(
                agreement_type=agreementtypeformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newagreementtype.save()
            return redirect("Master_details")

    return render(request, "master/master_details.html")


def Applicanttype_form(request):
    if request.method == "POST":
        applicanttypeformvalue = request.POST["ApplicantType"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["ApplicanttypeIdate"]
        if ApplicantType.objects.filter(applicant_type=applicanttypeformvalue).exists():
            messages.info(request, "Applicant Type already exists")
            return redirect("Master_details")
        else:
            newapplicanttype = ApplicantType.objects.create(
                applicant_type=applicanttypeformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newapplicanttype.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def AYyear_form(request):
    if request.method == "POST":
        ayyearformvalue = request.POST["AYyear"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["AYyearIdate"]
        if AYYear.objects.filter(ay_year=ayyearformvalue).exists():
            messages.info(request, "Ay Year already exists")
            return redirect("Master_details")
        else:
            newayyear = AYYear.objects.create(
                ay_year=ayyearformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newayyear.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def NatureOfBusiness_form(request):
    if request.method == "POST":
        natureofbusinessformvalue = request.POST["NatureBusiness"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["NatureOfBusinessIdate"]
        if NatureOfBusiness.objects.filter(
            nature_business=natureofbusinessformvalue
        ).exists():
            messages.info(request, "Nature of Business already exists")
            return redirect("Master_details")
        else:
            newnatureofbusiness = NatureOfBusiness.objects.create(
                nature_business=natureofbusinessformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newnatureofbusiness.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def PropertyIn_form(request):
    if request.method == "POST":
        propertyinformvalue = request.POST["PropertyIn"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["PropertyInIdate"]
        if PropertyIn.objects.filter(property_in=propertyinformvalue).exists():
            messages.info(request, "PropertyIn Business already exists")
            return redirect("Master_details")
        else:
            newpropertyin = PropertyIn.objects.create(
                property_in=propertyinformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newpropertyin.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def RejectionType_form(request):
    if request.method == "POST":
        rejectiontypeformvvalue = request.POST["Type"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["RejectionTypeIdate"]
        rejectiontypereasonformvvalue = request.POST["Reason"].strip()
        if RejectionType.objects.filter(
            rejection_type=rejectiontypeformvvalue,
            rejection_reason=rejectiontypereasonformvvalue,
        ).exists():
            messages.info(request, "Rejection type already exists")
            return redirect("Master_details")
        else:
            newrejectiontype = RejectionType.objects.create(
                rejection_type=rejectiontypeformvvalue,
                rejection_reason=rejectiontypereasonformvvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newrejectiontype.save()
            return redirect("Master_details")

    return render(request, "master/master_details.html")


def StageOfConstruction_form(request):
    if request.method == "POST":
        stageformvalue = request.POST["Stage"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["StageOfConstructionIdate"]
        if StageOfConstruction.objects.filter(stage=stageformvalue).exists():
            messages.info(request, "Stage Of Construction already exists")
            return redirect("Master_details")
        else:
            newstage = StageOfConstruction.objects.create(
                stage=stageformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newstage.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def Status_form(request):
    if request.method == "POST":
        statusformvalue = request.POST["Status"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["StatusIdate"]
        if Status.objects.filter(status=statusformvalue).exists():
            messages.info(request, "Status already exists")
            return redirect("Master_details")
        else:
            newstatus = Status.objects.create(
                status=statusformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newstatus.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def CompanyType_form(request):
    if request.method == "POST":
        companytypeformvalue = request.POST["CompanyType"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["CompanyTypeIdate"]
        if CompanyType.objects.filter(company_type=companytypeformvalue).exists():
            messages.info(request, "Company Type already exists")
            return redirect("Master_details")
        else:
            newcompanytype = CompanyType.objects.create(
                company_type=companytypeformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newcompanytype.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def CustomerType_form(request):
    if request.method == "POST":
        customertypeformvalue = request.POST["CustomerType"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["CustomerTypeIdate"]
        if CustomerType.objects.filter(cust_type=customertypeformvalue).exists():
            messages.info(request, "Customer Type already exists")
            return redirect("Master_details")
        else:
            newcustomertype = CustomerType.objects.create(
                cust_type=customertypeformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newcustomertype.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def DesignationType_form(request):
    if request.method == "POST":
        designationtypeformvalue = request.POST["DesignationType"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["DesignationTypeIdate"]
        if DesignationType.objects.filter(desg_type=designationtypeformvalue).exists():
            messages.info(request, "Designation Type already exists")
            return redirect("Master_details")
        else:
            newdesignationtype = DesignationType.objects.create(
                desg_type=designationtypeformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newdesignationtype.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def Product_form(request):
    if request.method == "POST":
        productformvalue = request.POST["Product"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["ProductIdate"]
        if Product.objects.filter(product=productformvalue).exists():
            messages.info(request, "Product already exists")
            return redirect("Master_details")
        else:
            newProduct = Product.objects.create(
                product=productformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newProduct.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def Profession_form(request):
    if request.method == "POST":
        professionformvalue = request.POST["Profession"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["ProfessionIdate"]
        if Profession.objects.filter(profession=professionformvalue).exists():
            messages.info(request, "Profession already exists")
            return redirect("Master_details")
        else:
            newprofession = Profession.objects.create(
                profession=professionformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newprofession.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def Qualification_form(request):
    if request.method == "POST":
        qualificationformvalue = request.POST["Qualification"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["QualificationIdate"]
        if Qualification.objects.filter(qualification=qualificationformvalue).exists():
            messages.info(request, "qualification already exists")
            return redirect("Master_details")
        else:
            newqualification = Qualification.objects.create(
                qualification=qualificationformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newqualification.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def Role_form(request):
    if request.method == "POST":
        roleformvalue = request.POST["Role"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["RoleIdate"]
        if Role.objects.filter(role=roleformvalue).exists():
            messages.info(request, "Role already exists")
            return redirect("Master_details")
        else:
            newrole = Role.objects.create(
                role=roleformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newrole.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def BankName_form(request):
    if request.method == "POST":
        banknameformvalue = request.POST.get("BankName")
        effective_date = date.today()
        ineffective_date = request.POST.get("BankNameIdate")
        if BankName.objects.filter(bank_name=banknameformvalue).exists():
            messages.info(request, "Bank Name already exists")
            return redirect("Master_details")
        else:
            newbankname = BankName.objects.create(
                bank_name=banknameformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newbankname.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def Degree_form(request):
    if request.method == "POST":
        degreeformvalue = request.POST["degree"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["DegreeIdate"]
        if Degree.objects.filter(degree=degreeformvalue).exists():
            messages.info(request, "Degree already exists")
            return redirect("Master_details")
        else:
            newdegree = Degree.objects.create(
                degree=degreeformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newdegree.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def LeadSource_form(request):
    if request.method == "POST":
        leadsourceformvalue = request.POST["leadSource"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["LeadSourceIdate"]
        if LeadSource.objects.filter(lead_source=leadsourceformvalue).exists():
            messages.info(request, "Degree already exists")
            return redirect("Master_details")
        else:
            newleadsource = LeadSource.objects.create(
                lead_source=leadsourceformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newleadsource.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def Nationality_form(request):
    if request.method == "POST":
        nationalityformvalue = request.POST["nation"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["NationalityIdate"]
        if Nationality.objects.filter(nationality=nationalityformvalue).exists():
            messages.info(request, "Degree already exists")
            return redirect("Master_details")
        else:
            newnationality = Nationality.objects.create(
                nationality=nationalityformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newnationality.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def ResidenceType_form(request):
    if request.method == "POST":
        residencetypeformvalue = request.POST["ResidenceType"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["ResidenceTypeIdate"]
        if ResidenceType.objects.filter(residence_type=residencetypeformvalue).exists():
            messages.info(request, "Residence Type already exists")
            return redirect("Master_details")
        else:
            newresidencetype = ResidenceType.objects.create(
                residence_type=residencetypeformvalue
            )
            newresidencetype.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def SalaryType_form(request):
    if request.method == "POST":
        salarytypeformvalue = request.POST.get("SalaryType").strip()
        effective_date = date.today()
        ineffective_date = request.POST["SalaryTypeIdate"]
        if SalaryType.objects.filter(salary_type=salarytypeformvalue).exists():
            messages.info(request, "Salary Type already exists")
            return redirect("Master_details")
        else:
            # newsalarytype = SalaryType.objects.create(
            #     salary_type=salarytypeformvalue, effective_date=effective_date, ineffective_date=ineffective_date)
            newsalarytype = SalaryType.objects.create(salary_type=salarytypeformvalue)
            newsalarytype.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def State_form(request):
    if request.method == "POST":
        stateformvalue = request.POST["state"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["StateIdate"]
        if State.objects.filter(state=stateformvalue).exists():
            messages.info(request, "State already exists")
            return redirect("Master_details")
        else:
            newstate = State.objects.create(
                state=stateformvalue,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newstate.save()
            return redirect("Master_details")
    return render(request, "master/master_details.html")


def SubProduct_form(request):
    if request.method == "POST":
        product = Product.objects.get(pk=int(request.POST["product"]))
        subproductformvalue = request.POST["SubProduct"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["SubProductIdate"]
        if SubProduct.objects.filter(
            sub_product=subproductformvalue, product=product
        ).exists():
            messages.info(request, "Sub Product already exists")
            return redirect("Master_details")
        else:
            newsubproduct = SubProduct.objects.create(
                sub_product=subproductformvalue,
                product=product,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newsubproduct.save()
            return redirect("Master_details")

    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "master/master_details.html", context=context)


def City_form(request):
    if request.method == "POST":
        state = State.objects.get(pk=int(request.POST["state"]))
        cityformvalue = request.POST["City"].strip()
        effective_date = date.today()
        ineffective_date = request.POST["CityIdate"]
        if City.objects.filter(city_name=cityformvalue, state=state).exists():
            messages.info(request, "city already exists")
            return redirect("Master_details")
        else:
            newcity = City.objects.create(
                city_name=cityformvalue,
                state=state,
                effective_date=effective_date,
                ineffective_date=ineffective_date,
            )
            newcity.save()
            return redirect("Master_details")

    states = State.objects.all()
    context = {"states": states}
    return render(request, "master/master_details.html", context=context)


@login_required(redirect_field_name="login", login_url="login")
def Masterdetails(request):
    # print(SubProduct.objects.all()[0].product.product)
    context = {
        "qualifications": Qualification.objects.all(),
        "professions": Profession.objects.all(),
        "roles": Role.objects.all(),
        "products": Product.objects.all(),
        "subproducts": SubProduct.objects.all(),
        "customertypes": CustomerType.objects.all(),
        "designationtypes": DesignationType.objects.all(),
        "company_types": CompanyType.objects.all(),
        "company_cat": CompanyCatergoryTypes.objects.all(),
        "company_names": CompanyName.objects.all(),
        "tenure": Tenure.objects.all(),
        "salarytypes": SalaryType.objects.all(),
        "residencetypes": ResidenceType.objects.all(),
        "banknames": BankName.objects.all(),
        "leadsources": LeadSource.objects.all(),
        "degrees": Degree.objects.all(),
        "nationalitys": Nationality.objects.all(),
        "states": State.objects.all(),
        "citys": City.objects.all(),
        "applicanttypes": ApplicantType.objects.all(),
        "propertyins": PropertyIn.objects.all(),
        "statues": Status.objects.all(),
        "natureofbusinesss": NatureOfBusiness.objects.all(),
        "ayyears": AYYear.objects.all(),
        "agreementtypes": AgreementType.objects.all(),
        "stageOfconstructions": StageOfConstruction.objects.all(),
        "rejectiontypes": RejectionType.objects.all(),
    }
    return render(request, "master/master_details.html", context=context)


def editqualification(request, id):
    if request.method == "POST":
        qualification = Qualification.objects.filter(id=id)
        newqualification = request.POST["Qualification"]
        qualification.update(qualification=newqualification)
        return redirect("Master_details")
    print(Qualification.objects.filter(id=id)[0])
    context = {"qualification": Qualification.objects.filter(id=id)[0]}
    return render(request, "master/qualification_edit.html", context=context)


def editprofession(request, id):
    if request.method == "POST":
        profession = Profession.objects.filter(id=id)
        newprofession = request.POST["Profession"]
        profession.update(profession=newprofession)
        return redirect("Master_details")
    print(Profession.objects.filter(id=id)[0])
    context = {"profession": Profession.objects.filter(id=id)[0]}
    return render(request, "master/profession_edit.html", context=context)


def editcompanyname(request, id):
    company_name = CompanyName.objects.get(pk=id)
    if request.method == "POST":
        company_name_updated = request.POST["Profession"]
        company_name.update(profession=company_name_updated)
        return redirect("Master_details")
    context = {"profession": company_name}
    return render(request, "master/companyname_edit.html", context=context)


def editcompanycat(request, id):
    company_cat = CompanyCatergoryTypes.objects.get(pk=id)
    if request.method == "POST":
        company_cat_updated = request.POST["Profession"]
        company_cat.update(cocat_type=company_cat_updated)
        return redirect("Master_details")
    context = {"profession": company_cat}
    return render(request, "master/companycat_edit.html", context=context)


def edittenure(request, id):
    tenure = Tenure.objects.get(pk=id)
    if request.method == "POST":
        tenure_updated = request.POST["Profession"]
        tenure.update(ten_type=tenure_updated)
        return redirect("Master_details")

    context = {"profession": tenure}
    return render(request, "master/tenure_edit.html", context=context)


def editrole(request, id):
    if request.method == "POST":
        role = Role.objects.filter(id=id)
        newrole = request.POST["Role"]
        role.update(role=newrole)
        return redirect("Master_details")
    print(Role.objects.filter(id=id)[0])
    context = {"role": Role.objects.filter(id=id)[0]}
    return render(request, "master/role_edit.html", context=context)


def editproduct(request, id):
    if request.method == "POST":
        product = Product.objects.filter(id=id)
        newproduct = request.POST["Product"]
        product.update(product=newproduct)
        return redirect("Master_details")
    print(Product.objects.filter(id=id)[0])
    context = {"product": Product.objects.filter(id=id)[0]}
    return render(request, "master/product_edit.html", context=context)


def editsubproduct(request, id):
    if request.method == "POST":
        sub_product = SubProduct.objects.filter(id=id)
        newsubproduct = request.POST["SubProduct"]
        sub_product.update(sub_product=newsubproduct)
        return redirect("Master_details")
    print(SubProduct.objects.filter(id=id)[0])
    context = {"product": SubProduct.objects.filter(id=id)[0]}
    return render(request, "master/subproduct_edit.html", context=context)


def editcustomertype(request, id):
    if request.method == "POST":
        cust_type = CustomerType.objects.filter(id=id)
        newcusttype = request.POST["CustomerType"]
        cust_type.update(cust_type=newcusttype)
        return redirect("Master_details")
    print(CustomerType.objects.filter(id=id)[0])
    context = {"cust_type": CustomerType.objects.filter(id=id)[0]}
    return render(request, "master/customertype_edit.html", context=context)


def editdesignationtype(request, id):
    if request.method == "POST":
        desg_type = DesignationType.objects.filter(id=id)
        newdesgtype = request.POST["DesignationType"]
        desg_type.update(desg_type=newdesgtype)
        return redirect("Master_details")
    print(DesignationType.objects.filter(id=id)[0])
    context = {"desg_type": DesignationType.objects.filter(id=id)[0]}
    return render(request, "master/designationtype_edit.html", context=context)


def editcompanytype(request, id):
    if request.method == "POST":
        company_type = CompanyType.objects.filter(id=id)
        newcomptype = request.POST["CompanyType"]
        company_type.update(company_type=newcomptype)
        return redirect("Master_details")
    print(CompanyType.objects.filter(id=id)[0])
    context = {"company_type": CompanyType.objects.filter(id=id)[0]}
    return render(request, "master/companytype_edit.html", context=context)


def editsalarytype(request, id):
    if request.method == "POST":
        salary_type = SalaryType.objects.filter(id=id)
        newsaltype = request.POST["salaryType"]
        salary_type.update(salary_type=newsaltype)
        return redirect("Master_details")
    print(SalaryType.objects.filter(id=id)[0])
    context = {"salary_type": SalaryType.objects.filter(id=id)[0]}
    return render(request, "master/salarytype_edit.html", context=context)


def editresidencetype(request, id):
    if request.method == "POST":
        residence_type = ResidenceType.objects.filter(id=id)
        newrestype = request.POST["resType"]
        residence_type.update(residence_type=newrestype)
        return redirect("Master_details")
    print(ResidenceType.objects.filter(id=id)[0])
    context = {"residence_type": ResidenceType.objects.filter(id=id)[0]}
    return render(request, "master/residencetype_edit.html", context=context)


def editbankname(request, id):
    if request.method == "POST":
        bank_name = BankName.objects.filter(id=id)
        newbankname = request.POST["bankName"]
        bank_name.update(bank_name=newbankname)
        return redirect("Master_details")
    print(BankName.objects.filter(id=id)[0])
    context = {"bank_name": BankName.objects.filter(id=id)[0]}
    return render(request, "master/editbankname.html", context=context)


def editleadsource(request, id):
    if request.method == "POST":
        lead_source = LeadSource.objects.filter(id=id)
        newleadsource = request.POST["leadSource"]
        lead_source.update(lead_source=newleadsource)
        return redirect("Master_details")
    print(LeadSource.objects.filter(id=id)[0])
    context = {"lead_source": LeadSource.objects.filter(id=id)[0]}
    return render(request, "master/leadsourceedit.html", context=context)


def editdegree(request, id):
    if request.method == "POST":
        degree = Degree.objects.filter(id=id)
        newdegree = request.POST["degree"]
        degree.update(degree=newdegree)
        return redirect("Master_details")
    print(Degree.objects.filter(id=id)[0])
    context = {"degree": Degree.objects.filter(id=id)[0]}
    return render(request, "master/degree_edit.html", context=context)


def editnationality(request, id):
    if request.method == "POST":
        nationality = Nationality.objects.filter(id=id)
        newnation = request.POST["nation"]
        nationality.update(nationality=newnation)
        return redirect("Master_details")
    print(Nationality.objects.filter(id=id)[0])
    context = {"nationality": Nationality.objects.filter(id=id)[0]}
    return render(request, "master/nationality_edit.html", context=context)


def editstate(request, id):
    if request.method == "POST":
        state = State.objects.filter(id=id)
        newstate = request.POST["state"]
        state.update(state=newstate)
        return redirect("Master_details")
    print(State.objects.filter(id=id)[0])
    context = {"state": State.objects.filter(id=id)[0]}
    return render(request, "master/state_edit.html", context=context)


def editcity(request, id):
    if request.method == "POST":
        city_name = City.objects.filter(id=id)
        newcity = request.POST["city"]
        city_name.update(city_name=newcity)
        return redirect("Master_details")
    print(City.objects.filter(id=id)[0])
    context = {"city_name": City.objects.filter(id=id)[0]}
    return render(request, "master/city_edit.html", context=context)


def editapplicanttype(request, id):
    if request.method == "POST":
        applicant_type = ApplicantType.objects.filter(id=id)
        newapplicant = request.POST["ApplicantType"]
        applicant_type.update(applicant_type=newapplicant)
        return redirect("Master_details")
    print(ApplicantType.objects.filter(id=id)[0])
    context = {"applicant_type": ApplicantType.objects.filter(id=id)[0]}
    return render(request, "master/applicant_edit.html", context=context)


def editpropertyln(request, id):
    if request.method == "POST":
        property_in = PropertyIn.objects.filter(id=id)
        newapropertyln = request.POST["PropertyIn"]
        property_in.update(property_in=newapropertyln)
        return redirect("Master_details")
    print(PropertyIn.objects.filter(id=id)[0])
    context = {"property_in": PropertyIn.objects.filter(id=id)[0]}
    return render(request, "master/propertyin_edit.html", context=context)


def editstatus(request, id):
    if request.method == "POST":
        status = Status.objects.filter(id=id)
        newstatus = request.POST["Status"]
        status.update(status=newstatus)
        return redirect("Master_details")
    print(Status.objects.filter(id=id)[0])
    context = {"status": Status.objects.filter(id=id)[0]}
    return render(request, "master/status_edit.html", context=context)


def editnatureofbusiness(request, id):
    if request.method == "POST":
        nature_business = NatureOfBusiness.objects.filter(id=id)
        newbusiness = request.POST["NatureBusiness"]
        nature_business.update(nature_business=newbusiness)
        return redirect("Master_details")
    print(NatureOfBusiness.objects.filter(id=id)[0])
    context = {"nature_business": NatureOfBusiness.objects.filter(id=id)[0]}
    return render(request, "master/natureofbusiness_edit.html", context=context)


def editayyear(request, id):
    if request.method == "POST":
        ay_year = AYYear.objects.filter(id=id)
        newayyear = request.POST["AyYear"]
        ay_year.update(ay_year=newayyear)
        return redirect("Master_details")
    print(AYYear.objects.filter(id=id)[0])
    context = {"ay_year": AYYear.objects.filter(id=id)[0]}
    return render(request, "master/ayyear_edit.html", context=context)


def editagreementtype(request, id):
    if request.method == "POST":
        agreement_type = AgreementType.objects.filter(id=id)
        newagreementtype = request.POST["AgreementType"]
        agreement_type.update(agreement_type=newagreementtype)
        return redirect("Master_details")
    print(AgreementType.objects.filter(id=id)[0])
    context = {"agreement_type": AgreementType.objects.filter(id=id)[0]}
    return render(request, "master/agreement_edit.html", context=context)


def editstageofconstruction(request, id):
    if request.method == "POST":
        stage = StageOfConstruction.objects.filter(id=id)
        newstage = request.POST["Stage"]
        stage.update(stage=newstage)
        return redirect("Master_details")
    print(StageOfConstruction.objects.filter(id=id)[0])
    context = {"stage": StageOfConstruction.objects.filter(id=id)[0]}
    return render(request, "master/stageofconstruction_edit.html", context=context)


def editrejectiontype(request, id):
    if request.method == "POST":
        rejection_type = RejectionType.objects.filter(id=id)
        newrejection = request.POST["Reason"]
        rejection_type.update(rejection_type=newrejection)
        return redirect("Master_details")
    print(RejectionType.objects.filter(id=id)[0])
    context = {"rejection_type": RejectionType.objects.filter(id=id)[0]}
    return render(request, "master/rejection_edit.html", context=context)


def Productandpolicy(request, action="no"):
    if not request.method == "POST":
        pass

    # action = request.GET['action']
    if action == "edit":
        id = int(action)
        product_and_policy_instance = product_and_policy_master.objects.get(pk=id)
        if product_and_policy_instance != "no":
            Productandpolicy_form = ProductAndPolicyMasterForm(
                instance=product_and_policy_instance
            )
            if not product_and_policy_instance.lock:
                if request.method == "POST":
                    current_value_form = ProductAndPolicyMasterForm(request.POST)
                    if current_value_form.is_valid():
                        current_instance = current_value_form.save(commit=False)
                        current_instance.pk = product_and_policy_instance.pk
                        current_instance.save()
                        messages.success(
                            request, "Product And Policy Details Updated Successfully"
                        )
                        return redirect("list_product_and_policy")
                    else:
                        messages.error(request, current_value_form.errors)
                else:
                    return redirect("add_products_and_policy_view")
                    return render(
                        request,
                        "master/add_product_and_policy.html",
                        context={"form": Productandpolicy_form, "id": id},
                    )
        else:
            return render(
                request,
                "master/add_product_and_policy.html",
                context={"form": ProductAndPolicyMasterForm(), "id": "no"},
            )
    else:
        if request.method == "POST":
            current_value_form = ProductAndPolicyMasterForm(request.POST)
            if current_value_form.is_valid():
                current_instance = current_value_form.save(commit=False)
                current_instance.save()
                messages.success(
                    request, " Product and Policy Details Added Successfully !"
                )
                return redirect("list_product_and_policy")
            else:
                messages.error(request, current_value_form.errors)
                return redirect("add_products_and_policy_view")
        else:
            context = {"form": ProductAndPolicyMasterForm(), "action": "new"}
            return render(request, "master/add_product_and_policy.html", context)

    # if request.method == 'POST':
    #     product = Product(
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

    #     return redirect('editProductsAndPolicy', id=product.prod_id)

    # context = {
    #     'banks': Bank.objects.all(),
    # }


def Productandpolicy_revieworedit(request, id):
    return render(request, "master/edit_products_and_policy.html")


def listProductAndPolicy(request):
    productAndPolicies = product_and_policy_master.objects.all()
    return render(
        request,
        "master/list_product_and_policy.html",
        context={"ProductsAndPolicy": productAndPolicies},
    )


def addProductAndPolicyView(request):

    if request.method == "POST":
        roi = request.POST.getlist("roi")
        # roi = int(roi)
        # if roi > 40:
        #     roi = roi / 100
        # effective_date = str(datetime.now())[:22]
        cocat_type_ = request.POST.getlist("cocat_type")
        min_loan_amount = request.POST.getlist("min_loan_amt")
        max_loan_amount = request.POST.getlist("max_loan_amt")
        co_type = request.POST.getlist("company_type")
        min_net_sal = request.POST.getlist("min_net_sal")
        max_net_sal = request.POST.getlist("max_net_sal")
        cutoff = request.POST.getlist("cutoff")
        salary_type_ = request.POST.getlist("salary_type")
        res_type_ = request.POST.getlist("res_type")
        tenure_ = request.POST.getlist("tenure")
        multiplier_number = request.POST.getlist("multiplier_number")

        print(request.POST)

        product_and_policy_instance = ProductAndPolicyMasterForm(request.POST)
        if product_and_policy_instance.is_valid():
            # product_and_policy_instance = product_and_policy_instance.save()
            product_and_policy_instance.effective_date = date.today().strftime(
                "%Y-%m-%d"
            )

            for company_type in co_type:
                com_type = CompanyType.objects.filter(company_type=company_type).first()
                product_and_policy_instance.company_type.add(com_type)

            for res_type in res_type_:
                residence_type = ResidenceType.objects.filter(
                    residence_type=res_type
                ).first()
                product_and_policy_instance.residence_type.add(residence_type)

            for sal_type in salary_type_:
                salary_type = SalaryType.objects.filter(salary_type=sal_type).first()
                product_and_policy_instance.salary_type.add(salary_type)

            for ten_type in tenure_:
                tenure_type = Tenure.objects.filter(ten_type=ten_type).first()
                product_and_policy_instance.tenure.add(tenure_type)

            for (min_sal, max_sal, cut_off) in zip(min_net_sal, max_net_sal, cutoff):

                if Foir.objects.filter(
                    min_amt=min_sal, max_amt=max_sal, cutoff=cut_off
                ).exists():
                    foir = Foir.objects.filter(
                        min_amt=min_sal, max_amt=max_sal, cutoff=cut_off
                    ).first()
                else:
                    foir = Foir.objects.create(
                        min_amt=min_sal, max_amt=max_sal, cutoff=cut_off
                    )
                product_and_policy_instance.foir.add(foir)

            for (cocat_type, multiplier_num, roi, min_loan_amnt, max_loan_amnt) in zip(
                cocat_type_, multiplier_number, roi, min_loan_amount, max_loan_amount
            ):
                print("Comm Comm i am here")
                if CompanyCategory.objects.filter(
                    cocat_type=cocat_type,
                    multiplier_number=multiplier_num,
                    roi=roi,
                    min_loan_amt=min_loan_amnt,
                    max_loan_amt=max_loan_amnt,
                ).exists():
                    company_category = CompanyCategory.objects.filter(
                        cocat_type=cocat_type,
                        multiplier_number=multiplier_num,
                        roi=roi,
                        min_loan_amt=min_loan_amnt,
                        max_loan_amt=max_loan_amnt,
                    ).first()

                else:
                    comp_category = CompanyCategory.objects.create(
                        cocat_type=cocat_type,
                        multiplier_number=multiplier_num,
                        roi=roi,
                        min_loan_amt=min_loan_amnt,
                        max_loan_amt=max_loan_amnt,
                    )

                product_and_policy_instance.company_category.add(comp_category)

            product_and_policy_instance.save()
            return redirect("list_product_and_policy")

        else:
            messages.error(request, product_and_policy_instance.errors)
            return redirect("add_products_and_policy_view")

    #         cocat_type = models.CharField(max_length=200)
    # multiplier_number = models.IntegerField()
    # roi = models.FloatField()
    # min_loan_amt = models.BigIntegerField()
    # max_loan_amt =

    context = {
        "form": ProductAndPolicyMasterForm(),
        "l_type": Product.objects.all(),
        "bank": BankName.objects.all(),
        "s_type": SalaryType.objects.all(),
        "res_type": ResidenceType.objects.all(),
        "des_type": DesignationType.objects.all(),
        "com_type": CompanyType.objects.all(),
        "cocatt_type": CompanyCatergoryTypes.objects.all(),
        "tenures": Tenure.objects.all(),
    }
    return render(request, "master/add_product_and_policy.html", context)


def deleteProductAndPolicy(request, id):

    product_and_policy_object = product_and_policy_master.objects.get(pk=id)
    product_and_policy_object.delete()
    messages.info(request, "Deleted Product and Policy Successfully.")
    return redirect("list_product_and_policy")
